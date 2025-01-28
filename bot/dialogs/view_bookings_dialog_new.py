from typing import Dict, List
from aiogram import F
from aiogram_dialog import Dialog, DialogManager, Window, SubManager
from aiogram_dialog.widgets.kbd import ListGroup, Row, Button
from aiogram_dialog.widgets.text import Const, Format, Case

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

import bot.database.booking_crud as booking_crud
from bot.utils import create_timeslot_str, send_error_report, short_day_of_week
from bot.database.schemas.booking_schema import BookingSchema
from bot.widgets.custom_cancel_widget import CustomCancel
from bot.constants import (
    BTN_CANCEL, ERROR_CANCEL_BOOKING, HEADER_USER_BOOKINGS, HEADER_USER_BOOKINGS_EMPTY,
    BTN_BACK, DATE_FORMAT, SUCCESS_CANCELED_BOOKING, BTN_FINISH
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
        "date": booking.date.strftime(DATE_FORMAT),
        "timeslot": create_timeslot_str(booking.start_time, booking.end_time),
    }

async def getter_user_bookings_window(**kwargs):
    dm: DialogManager = kwargs['dialog_manager']
    
    try:
        user_bookings = await booking_crud.get_bookings_by_username(dm.dialog_data["user"].username)
    except Exception as e:
        dm.done(result=e)
        
    formatted_bookings = [await format_booking(booking) for booking in user_bookings]
    dm.dialog_data["bookings"] = formatted_bookings
    dm.dialog_data["canceled_bookings"] = []
    return {
        "user": dm.dialog_data["user"],
        "bookings": formatted_bookings
    }

async def cancel_booking(callback: CallbackQuery, button: Button, submanager: SubManager):
    booking_id = int(submanager.item_id)
    
    try:
        booking = await booking_crud.get_booking_by_id(booking_id)
        submanager.manager.dialog_data["canceled_bookings"].append(booking)
        await booking_crud.delete_booking(booking_id)
    except Exception as e:
        canceled_bookings = submanager.manager.dialog_data["canceled_bookings"]
        submanager.manager.done(result=cancel_booking)
    

user_bookings_window = Window(
    Case(
        {
            False: Format(HEADER_USER_BOOKINGS_EMPTY),
            True: Format(HEADER_USER_BOOKINGS),
        },
        selector=F['dialog_data']['bookings'].len() > 0
    ),
    ListGroup(
        Row(
            Button(
                Format("{item[room]}"),
                id="booking_room"
            ),
            Button(
                Format("{item[date]}"),
                id="booking_dates"
            ),
            Button(
                Format("{item[timeslot]}"),
                id="booking_timeslot"
            ),
            Button(
                Const(BTN_CANCEL),
                id="delete_booking",
                on_click=cancel_booking
            ),
        ),
        id="user_bookings",
        items="bookings",
        item_id_getter=lambda item: item["id"]
    ),
    CustomCancel(Const(BTN_FINISH)),
    state=ViewBookingsDialogStates.VIEW_BOOKINGS,
    getter=getter_user_bookings_window
)

async def on_dialog_close(result: List[BookingSchema] | Exception, dm: DialogManager):
    if isinstance(result, Exception):
        await dm.event.message.answer(ERROR_CANCEL_BOOKING)
        dm.dialog_data["error_type"] = "Booking"
        await send_error_report(dm.event.bot, dm.dialog_data, str(result))
        return
    canceled_bookings_text = "\n".join(
        SUCCESS_CANCELED_BOOKING.format(
            room=booking.room,
            date=booking.date,
            formatted_day_of_week=short_day_of_week(booking.date),
            timeslot=create_timeslot_str(booking.start_time, booking.end_time),
            username=booking.username,
            user_full_name=booking.user_full_name,
        )
        for booking in result
    )
    await dm.event.message.answer(
        
    )

view_bookings_dialog = Dialog(
    user_bookings_window,
    on_start=on_dialog_start,
    on_close=on_dialog_close,
)
