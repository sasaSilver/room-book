from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Row, Calendar, CalendarConfig, Group, Back
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery, User
from aiogram.fsm.state import State, StatesGroup

from typing import TypedDict, Any
import datetime

from bot.widgets.custom_cancel_widget import CustomCancel
from bot.widgets.custom_timerange_widget import TimeRangeWidget
from bot.utils import (
    ShowDoneCondition, generate_timeslots, send_error_report, create_timeslot_str
)

class Booking(TypedDict):
    username: str
    user_id: int
    room: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time

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
    dialog_manager.dialog_data["selected_date"] = selected_date.isoformat()
    await dialog_manager.switch_to(BookingDialogStates.SELECT_BOOKING_TIME)

async def on_time_confirmed(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):         
    data = dialog_manager.dialog_data
    user: User = data["user"]
    #TODO implement api
    #success, error = await api_client.book(user.id, date, start, end)
    await callback.message.delete()
    success, error = True, "ErrorMsg"
    if not success:
        await callback.message.answer("<b><i>❌ Ошибка со стороны бота!</i></b>\nОтчет отправлен администратору.")
        await send_error_report(callback.bot, data, error)
        await dialog_manager.done(result=None)
        return
    timeslot_text = create_timeslot_str(data["time_start"], data["time_end"])
    booking = Booking(
        username=user.username,
        user_id=user.id,
        room=data["selected_room"],
        date=data["selected_date"],
        start_time=data["time_start"],
        end_time=data["time_end"]
    )
    await callback.message.answer(
        f"<b>✅ {data['selected_room']} на {data['selected_date']}, {timeslot_text} была забронирована "
        f"<a href='https://t.me/{user.username}'>{user.full_name}</a></b>."
    )
    await dialog_manager.done(result=booking)

async def reset_time_selection(_callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
    time_selection_widget = dialog_manager.find("time_selection")
    time_selection_widget.reset(dialog_manager)
    dialog_manager.dialog_data.pop("time_start")
    dialog_manager.dialog_data.pop("time_end")


async def getter_date_selection(dialog_manager: DialogManager, **_kwargs):
    room = dialog_manager.dialog_data["selected_room"]
    return {
        "selected_room": room
    }

async def getter_time_selection(dialog_manager: DialogManager, **_kwargs):
    data = dialog_manager.dialog_data
    # TODO implement api for data["daily_bookings"]
    daily_bookings = {}
    return {
        "selected_date": data["selected_date"],
        "selected_room": data["selected_room"],
        "daily_bookings": daily_bookings
    }

select_room_window = Window(
    Const("Выберите аудиторию:"),
    Row(
        Button(Const("Аудитория A"), id="btn_room_a", on_click=on_room_selected),
        Button(Const("Аудитория B"), id="btn_room_b", on_click=on_room_selected),
        Button(Const("Аудитория C"), id="btn_room_c", on_click=on_room_selected),
    ),
    CustomCancel(Const("❌")),
    state=BookingDialogStates.SELECT_ROOM
)

select_date_window = Window(
    Format("Выберите дату брони для <b>{selected_room}</b>:"),
    Calendar(
        id="calendar",
        on_click=on_date_selected,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    Row(
        Back(Const("🔙")),
        CustomCancel(Const("❌")),
    ),
    getter=getter_date_selection,
    state=BookingDialogStates.SELECT_DATE,
)

time_selection_widget = TimeRangeWidget(
    timepoints=generate_timeslots(datetime.time(7, 0), datetime.time(18, 30), 30),
    id="time_selection"
)

select_time_window = Window(
    Format("Выберите время начала и конца брони <b>{selected_room}</b> на <b>{selected_date}</b>:"),
    Group(time_selection_widget, width=4),
    Row(
        Back(Const("🔙"), on_click=reset_time_selection),
        Button(
            Const("✅ Завершить"),
            id="btn_time_selected",
            on_click=on_time_confirmed,
            when=ShowDoneCondition()
        ),
    ),
    CustomCancel(Const("❌")),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=getter_time_selection
)

async def on_dialog_close(result: dict | None, dialog_manager: DialogManager):
    print(f"Booking dialog closed. Result: {result}")   

booking_dialog = Dialog(
    select_room_window,
    select_date_window,
    select_time_window,
    on_start=on_dialog_start,
    on_close=on_dialog_close,
)
