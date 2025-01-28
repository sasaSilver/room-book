from typing import List, Dict
from aiogram_dialog import Dialog, DialogManager, Window, SubManager
from aiogram_dialog.widgets.kbd import ListGroup, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

import bot.database.booking_crud as booking_crud
from bot.utils import send_error_report
from bot.database.schemas.booking_schema import BookingSchema

class ViewBookingsDialogStates(StatesGroup):
    VIEW_BOOKINGS = State()
    
async def on_dialog_start(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["user"] = dialog_manager.start_data["user"]
    
async def format_booking(booking: BookingSchema) -> Dict[str, str]:
    room_text = booking.room if len(booking.room) <= 7 else f"{booking.room[:6]}.{booking.room[-1]}"
    return {
        "id": booking.id,
        "room": booking.room,
        "booking_details": (
            f"{room_text}, "
            f"{booking.date.strftime('%d.%m')}: "
            f"{booking.start_time.strftime('%H:%M')}-{booking.end_time.strftime('%H:%M')}"
        )
    }

async def getter_user_bookings_window(**kwargs):
    dm: DialogManager = kwargs['dialog_manager']
    result = await booking_crud.get_bookings_by_username(dm.dialog_data["user"].username)
    if isinstance(result, Exception):
        await dm.event.answer(
            "<b><i>❌ Произошла ошибка со стороны бота!</i></b>\n"
            "Отчет отправлен администратору."
        )
        await send_error_report(dm.event.bot, dm.dialog_data, str(result))
        await dm.done()
    
    formatted_bookings = [await format_booking(booking) for booking in result]
    dm.dialog_data["bookings"] = formatted_bookings
    return {
        "user": dm.dialog_data["user"],
        "bookings": formatted_bookings
    }

async def on_delete_booking(callback: CallbackQuery, button: Button, manager: SubManager):
    booking_id = int(manager.item_id)
    result = await booking_crud.delete_booking(booking_id)
    if isinstance(result, Exception):
        await manager.event.message.answer(
            "<b><i>❌ При удалении бронирования произошла ошибка со стороны бота!</i></b>\n"
            "Отчет отправлен администратору."
        )
        await send_error_report(manager.event.bot, manager.dialog_data, str(result))
        await manager.done()
    
    

user_bookings_window = Window(
    Format(
        "Бронирования пользователя <a href='https://t.me/{user.username}'>{user.full_name}</a>",
    ),
    ListGroup(
        Row(
            Button(
                Format("{item[booking_details]}"),
                id="booking_details"
            ),
            Button(
                Const("❌"),
                id="delete_booking",
                on_click=on_delete_booking
            ),
        ),
        id="user_bookings",
        items="bookings",
        item_id_getter=lambda item: item["id"]
    ),
    state=ViewBookingsDialogStates.VIEW_BOOKINGS,
    getter=getter_user_bookings_window
)

view_bookings_dialog = Dialog(
    user_bookings_window,
    on_start=on_dialog_start
)
