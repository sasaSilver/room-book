from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button, Row, Calendar, CalendarConfig, Group, Back
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

import datetime

from custom_cancel_wdget import CustomCancel
from custom_timerange_widget import TimeRangeWidget
from show_done_predicate import ShowDoneCondition

class BookingDialogStates(StatesGroup):
    SELECT_ROOM = State()
    SELECT_DATE = State()
    SELECT_BOOKING_TIME = State()
    BOOKING_SUCCESS = State()
    BOOKING_FAILURE = State()
    

async def on_room_selected(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["selected_room"] = button.text.text
    await dialog_manager.switch_to(BookingDialogStates.SELECT_DATE)

async def on_date_selected(
        callback_query: CallbackQuery,
        calendar: Calendar,
        dialog_manager: DialogManager,
        selected_date: datetime.date
):
    dialog_manager.dialog_data["selected_date"] = selected_date.isoformat()
    await dialog_manager.switch_to(BookingDialogStates.SELECT_BOOKING_TIME)

async def on_time_confirmed(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
    await callback.message.delete()
     
    chosen_timeslots = time_selection_widget.get_selected_time_points(dialog_manager)
    
    if len(chosen_timeslots) != 2:
        await callback.message.answer("Выберите <b>оба<b/> временных интервала <b>начала и конца брони</b>.")
        return
    room = dialog_manager.dialog_data["selected_room"]
    start, end = chosen_timeslots
    #TODO implement api
    #success, error = await api_client.book(callback.from_user.id, date, start, end)
    success = True
    error = "ErrorText"
    if success:
        await dialog_manager.switch_to(BookingDialogStates.BOOKING_SUCCESS)
    else:
        await dialog_manager.switch_to(BookingDialogStates.BOOKING_FAILURE)
        await callback.message.answer(
            f"<b>Возникла ошибка: {error}</b>\nНапишите @ob0china на Telegram и сообщите об ошибке."
        )
        widget = dialog_manager.find("time_selection")
        widget.reset(dialog_manager)

async def reset_time_selection(callback: CallbackQuery, _button: Button, dialog_manager: DialogManager):
    widget = dialog_manager.find("time_selection")
    if widget:
        widget.reset(dialog_manager)
    # Clear data
    dialog_manager.dialog_data.pop("time_start")
    dialog_manager.dialog_data.pop("time_end")
    

async def getter_for_date_selection(dialog_manager: DialogManager, **_kwargs) -> dict:
    room = dialog_manager.dialog_data["selected_room"]
    return {
        "selected_room": room
    }

async def getter_for_time_selection(dialog_manager: DialogManager, **_kwargs) -> dict:
    data = dialog_manager.dialog_data
    _, data["daily_bookings"] = 0, {}
    return {
        "selected_date": data["selected_date"],
        "selected_room": data["selected_room"],
         #TODO implement api for data["daily_bookings"]
        "daily_bookings": data["daily_bookings"]
    }

async def getter_for_booking_success(dialog_manager: DialogManager, **_kwargs) -> dict:
    data = dialog_manager.dialog_data
    time_start = data["time_start"]
    time_start = datetime.time.fromisoformat(time_start).strftime("%H:%M")
    time_end = data["time_end"]
    time_end = datetime.time.fromisoformat(time_end).strftime("%H:%M")
    
    return {
        "selected_date": data["selected_date"],
        "timeslot_text": f"{time_start} - {time_end}",
        "selected_room": data["selected_room"],
        "user": dialog_manager.event.from_user
    }

def generate_timeslots(start_time: datetime.time, end_time: datetime.time, interval: int) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots


select_room_window = Window(
    Const("Выберите аудиторию:"),
    Row(
        Button(Const("Аудитория A"), id="btn_room_a", on_click=on_room_selected),
        Button(Const("Аудитория B"), id="btn_room_b", on_click=on_room_selected),
        Button(Const("Аудитория C"), id="btn_room_c", on_click=on_room_selected),
    ),
    CustomCancel(),
    state=BookingDialogStates.SELECT_ROOM,
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
        CustomCancel(),
    ),
    getter=getter_for_date_selection,
    state=BookingDialogStates.SELECT_DATE,
)

time_selection_widget = TimeRangeWidget(
    timepoints=generate_timeslots(datetime.time(7, 0), datetime.time(18, 30), 30),
    id="time_selection",
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
    CustomCancel(),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=getter_for_time_selection
)

booking_success_window = Window(
    Format(
        "<b>{selected_room} на {selected_date}, {timeslot_text} была забронирована <a href='https://t.me/{user.username}'>{user.full_name}</a></b>."
    ),
    getter=getter_for_booking_success,
    state=BookingDialogStates.BOOKING_SUCCESS
)

booking_dialog = Dialog(select_room_window, select_date_window, select_time_window, booking_success_window)