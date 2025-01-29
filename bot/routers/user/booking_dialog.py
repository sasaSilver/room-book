from aiogram import F
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Row, Calendar, CalendarConfig, Group, Back
)
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram.types import CallbackQuery, User
from aiogram.fsm.state import State, StatesGroup

import datetime

from bot.widgets.custom_cancel_widget import CustomCancel
from bot.widgets.custom_timerange_widget import TimeRangeWidget
from bot.utils import (
    generate_timeslots, send_error_report, create_timeslot_str, short_day_of_week
)
import bot.database.db_crud as db_crud
from bot.database.schemas import BookingSchema
from bot.constants import (
    AVAILABLE_ROOMS, START_TIME, END_TIME, TIMESLOT_DURATION,
    SELECT_ROOM_TEXT, SELECT_DATE_TEMPLATE, SELECT_TIME_TEMPLATE, SELECT_TIME_EMPTY_TEMPLATE,
    BTN_CANCEL_TEXT, BTN_BACK_TEXT, BTN_FINISH_TEXT,
    SUCCESS_BOOKING_TEMPLATE,
    ERROR_BOOKING_TEXT
)

class BookingDialogStates(StatesGroup):
    SELECT_ROOM = State()
    SELECT_DATE = State()
    SELECT_BOOKING_TIME = State()
    
async def fetch_user(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["user"] = dialog_manager.start_data["user"]
    
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
    user: User = data["user"]
    
    booking = BookingSchema(
        username=user.username,
        user_full_name=user.full_name,
        room=data["selected_room"],
        date=data["selected_date"],
        start_time=datetime.time.fromisoformat(data["start_time"]),
        end_time=datetime.time.fromisoformat(data["end_time"])
    )
    
    try:
        await db_crud.create_booking(booking)
    except Exception as e:
        await dialog_manager.done(result=e)
    
    await dialog_manager.done(result=booking)
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
    
    try:
        daily_bookings = await db_crud.get_bookings_by_date_room(
            data["selected_date"], data["selected_room"]
        )
        print("FETCHED BOOKINGS")
    except Exception as e:
        await dialog_manager.done(result=e)
        
    partial_result["daily_bookings"] = daily_bookings
    dialog_manager.dialog_data["cached_bookings"] = daily_bookings
    return partial_result

select_room_window = Window(
    Const(SELECT_ROOM_TEXT),
    Row(*[
        Button(Const(room), id=f"btn_room", on_click=select_this_room)
          for room in AVAILABLE_ROOMS
    ]),
    CustomCancel(Const(BTN_CANCEL_TEXT)),
    state=BookingDialogStates.SELECT_ROOM
)

select_date_window = Window(
    Format(SELECT_DATE_TEMPLATE),
    Calendar(
        id="calendar",
        on_click=select_chosen_date,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    Row(
        Back(Const(BTN_BACK_TEXT)),
        CustomCancel(Const(BTN_CANCEL_TEXT)),
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
            0: Format(SELECT_TIME_EMPTY_TEMPLATE),
            1: Format(SELECT_TIME_TEMPLATE)
        },
        selector="has_timeslots"
    ),
    Group(time_selection_widget, width=4),
    Row(
        Back(Const(BTN_BACK_TEXT), on_click=clear_date_time_cache),
        Button(
            Const(BTN_FINISH_TEXT),
            id="btn_time_selected",
            on_click=create_booking,
            when=F["dialog_data"]["start_time"] and F["dialog_data"]["end_time"]
        ),
    ),
    CustomCancel(Const(BTN_CANCEL_TEXT)),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=get_daily_bookings
)

async def on_dialog_close(result: BookingSchema | Exception, dm: DialogManager):
    if isinstance(error := result, Exception):
        await dm.event.message.answer(ERROR_BOOKING_TEXT)
        dm.dialog_data["error_type"] = "Booking"
        await send_error_report(dm.event.bot, dm.dialog_data, str(error))
    elif isinstance(booking := result, BookingSchema):
        timeslot_text = create_timeslot_str(booking.start_time, booking.end_time)
        await dm.event.message.answer(
            SUCCESS_BOOKING_TEMPLATE.format(
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
    on_start=fetch_user,
    on_close=on_dialog_close,
)
