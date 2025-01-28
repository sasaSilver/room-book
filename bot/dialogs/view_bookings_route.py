from typing import Dict
from aiogram import F
from aiogram_dialog import Dialog, DialogManager, Window, SubManager
from aiogram_dialog.widgets.kbd import ListGroup, Row, Button, Back
from aiogram_dialog.widgets.text import Const, Format

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

import bot.database.booking_crud as booking_crud
from bot.utils import send_error_report
from bot.database.schemas.booking_schema import BookingSchema
from bot.widgets.custom_cancel_widget import CustomCancel
from bot.constants import (
    BTN_CANCEL, HEADER_USER_BOOKINGS, HEADER_NO_BOOKINGS,
    BTN_BACK, ERROR_BOT, ERROR_DELETE_BOOKING,
    DATE_FORMAT, TIME_FORMAT
)

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
            f"{booking.date.strftime(DATE_FORMAT)}: "
            f"{booking.start_time.strftime(TIME_FORMAT)}-{booking.end_time.strftime(TIME_FORMAT)}"
        )
    }

async def getter_user_bookings_window(**kwargs):
    dm: DialogManager = kwargs['dialog_manager']
    result = await booking_crud.get_bookings_by_username(dm.dialog_data["user"].username)
    if isinstance(result, Exception):
        await dm.event.answer(ERROR_BOT)
        await send_error_report(dm.event.bot, dm.dialog_data, str(result))
        await dm.done()
    
    formatted_bookings = [await format_booking(booking) for booking in result]
    dm.dialog_data["bookings"] = formatted_bookings
    return {
        "user": dm.dialog_data["user"],
        "bookings": formatted_bookings
    }

async def delete_booking(callback: CallbackQuery, button: Button, manager: SubManager):
    booking_id = int(manager.item_id)
    result = await booking_crud.delete_booking(booking_id)
    if isinstance(result, Exception):
        await manager.event.message.answer(ERROR_DELETE_BOOKING)
        await send_error_report(manager.event.bot, manager.dialog_data, str(result))
        await manager.done()

user_bookings_window = Window(
    Format(
        HEADER_USER_BOOKINGS,
        when=F['dialog_data']['bookings'].len() > 0
    ),
    Format(
        HEADER_NO_BOOKINGS,
        when=F['dialog_data']['bookings'].len() == 0
    ),
    ListGroup(
        Row(
            Button(
                Format("{item[booking_details]}"),
                id="booking_details"
            ),
            Button(
                Const(BTN_CANCEL),
                id="delete_booking",
                on_click=delete_booking
            ),
        ),
        id="user_bookings",
        items="bookings",
        item_id_getter=lambda item: item["id"]
    ),
    CustomCancel(Const(BTN_BACK)),
    state=ViewBookingsDialogStates.VIEW_BOOKINGS,
    getter=getter_user_bookings_window
)

view_bookings_dialog = Dialog(
    user_bookings_window,
    on_start=on_dialog_start
)
