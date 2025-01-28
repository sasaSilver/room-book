from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Row, Calendar, CalendarConfig, Group, Back
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery, User
from aiogram.fsm.state import State, StatesGroup

import datetime

from bot.widgets.custom_cancel_widget import CustomCancel
from bot.widgets.custom_timerange_widget import TimeRangeWidget
from bot.utils import (
    ShowDoneCondition, generate_timeslots, send_error_report, create_timeslot_str, short_day_of_week
)
import bot.database.booking_crud as booking_crud
from bot.database.schemas import BookingSchema
from bot.constants import (
    HEADER_SELECT_ROOM, HEADER_SELECT_DATE, HEADER_SELECT_TIME,
    BTN_CANCEL, BTN_BACK, BTN_FINISH,
    ERROR_CREATE_BOOKING, ROOMS, SUCCESS_BOOKING,
)

class BookingDialogStates(StatesGroup):
    SELECT_ROOM = State()
    SELECT_DATE = State()
    SELECT_BOOKING_TIME = State()
    
async def on_dialog_start(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["user"] = dialog_manager.start_data["user"]
    
async def on_room_selected(_callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["selected_room"] = button.text.text
    await dialog_manager.switch_to(BookingDialogStates.SELECT_DATE)

async def on_date_selected(
        callback: CallbackQuery,
        _calendar: Calendar,
        dialog_manager: DialogManager,
        selected_date: datetime.date
):
    callback.message.delete()
    dialog_manager.dialog_data["selected_date"] = selected_date
    await dialog_manager.switch_to(BookingDialogStates.SELECT_BOOKING_TIME)

async def on_time_confirmed(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):         
    await callback.message.delete()
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
        await booking_crud.create_booking(booking)
    except Exception as e:
        await dialog_manager.done(result=e)
        return
    await dialog_manager.done(result=booking)

async def reset_time_selection(_callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
    time_selection_widget = dialog_manager.find("time_selection")
    time_selection_widget.reset(dialog_manager)
    dialog_manager.dialog_data.pop("start_time", None)
    dialog_manager.dialog_data.pop("end_time", None)

async def getter_date_selection(dialog_manager: DialogManager, **_kwargs):
    room = dialog_manager.dialog_data["selected_room"]
    return {
        "selected_room": room
    }

async def getter_time_selection(dialog_manager: DialogManager, **_kwargs):
    data = dialog_manager.dialog_data
    result = await booking_crud.get_bookings_by_date_room(
        data["selected_date"],
        data["selected_room"]
    )
    if isinstance(result, Exception):
        await dialog_manager.done(result=result)
        return
    return {
        "selected_date": data["selected_date"],
        "formatted_day_of_week": short_day_of_week(data["selected_date"]),
        "selected_room": data["selected_room"],
        "daily_bookings": result
    }

select_room_window = Window(
    Const(HEADER_SELECT_ROOM),
    Row(*[
        Button(Const(room), id=f"room_{i}", on_click=on_room_selected)
          for i, room in enumerate(ROOMS)
    ]),
    CustomCancel(Const(BTN_CANCEL)),
    state=BookingDialogStates.SELECT_ROOM
)

select_date_window = Window(
    Format(HEADER_SELECT_DATE),
    Calendar(
        id="calendar",
        on_click=on_date_selected,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    Row(
        Back(Const(BTN_BACK)),
        CustomCancel(Const(BTN_CANCEL)),
    ),
    getter=getter_date_selection,
    state=BookingDialogStates.SELECT_DATE,
)

time_selection_widget = TimeRangeWidget(
    timepoints=generate_timeslots(datetime.time(7, 0), datetime.time(18, 30), 30),
    id="time_selection"
)

select_time_window = Window(
    Format(HEADER_SELECT_TIME),
    Group(time_selection_widget, width=4),
    Row(
        Back(Const(BTN_BACK), on_click=reset_time_selection),
        Button(
            Const(BTN_FINISH),
            id="btn_time_selected",
            on_click=on_time_confirmed,
            when=ShowDoneCondition()
        ),
    ),
    CustomCancel(Const(BTN_CANCEL)),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=getter_time_selection
)

async def on_dialog_close(result: BookingSchema | Exception, dm: DialogManager):
    if isinstance(result, Exception):
        await dm.event.message.answer(ERROR_CREATE_BOOKING)
        dm.dialog_data["error_type"] = "Booking"
        await send_error_report(dm.event.bot, dm.dialog_data, str(result))
    elif isinstance(result, BookingSchema):
        timeslot_text = create_timeslot_str(result.start_time, result.end_time)
        await dm.event.message.answer(
            SUCCESS_BOOKING.format(
                room=result.room,
                date=result.date,
                formatted_day_of_week=short_day_of_week(result.date),
                timeslot=timeslot_text,
                username=result.username,
                user_full_name=result.user_full_name
            )
        )

booking_dialog = Dialog(
    select_room_window,
    select_date_window,
    select_time_window,
    on_start=on_dialog_start,
    on_close=on_dialog_close,
)
