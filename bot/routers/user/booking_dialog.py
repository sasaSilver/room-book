from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Row, Calendar, CalendarConfig, Group, Back
)
from aiogram_dialog.widgets.text import Const, Format, Case

from aiogram.types import CallbackQuery, User
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

import datetime
from typing import Optional

from bot.widgets.custom_cancel_widget import CustomCancel
from bot.widgets.custom_timerange_widget import TimeRangeWidget
from bot.utils import (
    generate_timeslots, create_timeslot_str, short_day_of_week
)
import bot.database.db_crud as db_crud
from bot.database.schemas import BookingSchema
from bot.constants import (
    EMOJI, TEXT, TEMPLATE, BTN_TEXT,
    AVAILABLE_ROOMS, START_TIME, END_TIME, TIMESLOT_DURATION
)

class BookingDialogStates(StatesGroup):
    SELECT_ROOM = State()
    SELECT_DATE = State()
    SELECT_BOOKING_TIME = State()
    
async def select_this_room(_callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["selected_room"] = button.text.text
    await dialog_manager.switch_to(BookingDialogStates.SELECT_DATE)

async def select_chosen_date(
        callback: CallbackQuery,
        _calendar: Calendar,
        dialog_manager: DialogManager,
        selected_date: datetime.date
):
    dialog_manager.dialog_data["selected_date"] = selected_date
    await dialog_manager.switch_to(BookingDialogStates.SELECT_BOOKING_TIME)
    callback.message.delete()

async def create_booking(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):         
    data = dialog_manager.dialog_data
    user: User = dialog_manager.event.from_user
    
    booking = BookingSchema(
        username=user.username,
        user_full_name=user.full_name,
        room=data["selected_room"],
        date=data["selected_date"],
        start_time=datetime.time.fromisoformat(data["start_time"]),
        end_time=datetime.time.fromisoformat(data["end_time"])
    )
    
    await db_crud.create_booking(booking)
    
    await dialog_manager.done(result=booking)
    await callback.answer(EMOJI.TICK)
    await callback.message.delete()

async def clear_date_time_cache(_callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
    time_selection_widget: TimeRangeWidget = dialog_manager.find("time_selection")
    time_selection_widget.reset(dialog_manager)
    dialog_manager.dialog_data.pop("start_time", None)
    dialog_manager.dialog_data.pop("end_time", None)
    dialog_manager.dialog_data.pop("cached_bookings", None)

async def get_selected_room(dialog_manager: DialogManager, **_kwargs):
    room = dialog_manager.dialog_data["selected_room"]
    return {
        "selected_room": room
    }

async def get_daily_bookings(dialog_manager: DialogManager, **_kwargs):
    data = dialog_manager.dialog_data
    
    now = datetime.datetime.now()
    has_timeslots = now < datetime.datetime.combine(data["selected_date"], END_TIME)
    
    partial_result = {
        "selected_date": data["selected_date"],
        "formatted_day_of_week": short_day_of_week(data["selected_date"]),
        "selected_room": data["selected_room"],
        "has_timeslots": has_timeslots,
        "daily_bookings": None,
    }
    
    if "cached_bookings" in data:
        partial_result["daily_bookings"] = data["cached_bookings"]
        return partial_result
    
    daily_bookings = await db_crud.get_bookings_by_date_room(
        data["selected_date"], data["selected_room"]
    )
    
    partial_result["daily_bookings"] = daily_bookings
    dialog_manager.dialog_data["cached_bookings"] = daily_bookings
    # store fetched bookings as "cache" in dialog data to not refetch on window re-render
    return partial_result

select_room_window = Window(
    Const(TEXT.SELECT_ROOM),
    Row(*[
        Button(Const(room), id=f"btn_room_{i}", on_click=select_this_room)
          for i, room in enumerate(AVAILABLE_ROOMS)
    ]),
    CustomCancel(Const(BTN_TEXT.CANCEL)),
    state=BookingDialogStates.SELECT_ROOM
)

select_date_window = Window(
    Format(TEMPLATE.SELECT_DATE),
    Calendar(
        id="calendar",
        on_click=select_chosen_date,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    Row(
        Back(Const(BTN_TEXT.BACK)),
        CustomCancel(Const(BTN_TEXT.CANCEL)),
    ),
    getter=get_selected_room,
    state=BookingDialogStates.SELECT_DATE,
)

time_selection_widget = TimeRangeWidget(
    timepoints=generate_timeslots(START_TIME, END_TIME, TIMESLOT_DURATION),
    id="time_selection"
)

select_time_window = Window(
    Case(
        {
            0: Format(TEMPLATE.SELECT_TIME_EMPTY),
            1: Format(TEMPLATE.SELECT_TIME),
        },
        selector="has_timeslots"
    ),
    Group(time_selection_widget, width=4),
    Row(
        Back(Const(BTN_TEXT.BACK), on_click=clear_date_time_cache),
        Button(
            Const(BTN_TEXT.FINISH),
            id="btn_time_selected",
            on_click=create_booking,
            when=F["dialog_data"]["start_time"] and F["dialog_data"]["end_time"]
        ),
    ),
    CustomCancel(Const(BTN_TEXT.CANCEL)),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=get_daily_bookings
)

async def on_dialog_close(result: Optional[BookingSchema], dm: DialogManager):
    if not isinstance(result, BookingSchema):
        return
    
    booking = result
    timeslot_text = create_timeslot_str(booking.start_time, booking.end_time)
    await dm.event.message.answer(
        TEMPLATE.SUCCESS_BOOKING.format(
            room=booking.room,
            date=booking.date,
            formatted_day_of_week=short_day_of_week(booking.date),
            timeslot=timeslot_text,
            username=booking.username,
            user_full_name=booking.user_full_name
        )
    )

booking_dialog = Dialog(
    select_room_window,
    select_date_window,
    select_time_window,
    on_close=on_dialog_close,
)
