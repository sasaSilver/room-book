from aiogram_dialog import Dialog, DialogManager, Window, SubManager
from aiogram_dialog.widgets.kbd import ListGroup, Row, Button, Checkbox, ManagedCheckbox, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Case

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from typing import Any, Dict, List, Optional

import bot.database.db_crud as db_crud
from bot.utils import create_timeslot_str, send_error_report, short_day_of_week
from bot.database.schemas.booking_schema import BookingSchema
from bot.constants import TEXT, TEMPLATE, BTN_TEXT, FORMAT
from bot.widgets.custom_cancel_widget import CustomCancel

class ViewBookingsDialogStates(StatesGroup):
    VIEW_BOOKINGS = State()
    
async def on_dialog_start(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["user"] = dialog_manager.start_data["user"]
    dialog_manager.dialog_data["bookings_to_cancel"] = []
    
def format_booking(booking: BookingSchema) -> Dict[str, str]:
    return {
        "id": booking.id,
        "room": booking.room,
        "booking_details": (
            f"{booking.date.strftime(FORMAT.DATE)}\n"
            f"{booking.start_time.strftime(FORMAT.TIME)}-{booking.end_time.strftime(FORMAT.TIME)}"
        )
    }

async def fetch_user_bookings(**kwargs):
    dm: DialogManager = kwargs['dialog_manager']

    if formatted_bookings := dm.dialog_data.get("cached_bookings", False):
        return {
            "user": dm.dialog_data["user"],
            "bookings": dm.dialog_data["cached_bookings"]
        }
    
    user_bookings = await db_crud.get_bookings_by_username(dm.dialog_data["user"].username)
        
    formatted_bookings = [format_booking(booking) for booking in user_bookings]
    dm.dialog_data["cached_bookings"] = formatted_bookings
    return {
        "user": dm.dialog_data["user"],
        "bookings": formatted_bookings
    }

async def flag_booking_for_cancel(_callback: CallbackQuery, button: ManagedCheckbox, submanager: SubManager):
    booking_id = int(submanager.item_id)
    if button.is_checked():
        submanager.manager.dialog_data["bookings_to_cancel"].append(booking_id)
    else:
        submanager.manager.dialog_data["bookings_to_cancel"].remove(booking_id)
    

user_bookings_window = Window(
    Case(
        {
            True: Format(TEMPLATE.USER_BOOKINGS),
            False: Format(TEMPLATE.USER_BOOKINGS_EMPTY),
        },
        selector=F['bookings'].len() > 0
    ),
    
    ListGroup(
        Button(Format("{item[room]}"), id="booking_room"),
        Button(Format("{item[booking_details]}"), id="booking_details"),
        Checkbox(
            Const(BTN_TEXT.CANCELLED),
            Const(BTN_TEXT.CANCEL),
            id="btn_cancel",
            on_state_changed=flag_booking_for_cancel
        ),
        id="user_bookings",
        items="bookings",
        item_id_getter=lambda item: item["id"]
    ),
    CustomCancel(Const(BTN_TEXT.FINISH)),
    state=ViewBookingsDialogStates.VIEW_BOOKINGS,
    getter=fetch_user_bookings
)

async def on_dialog_close(result: Optional[Any], dm: DialogManager):
    booking_ids_to_cancel = dm.dialog_data["bookings_to_cancel"]
    if len(booking_ids_to_cancel) == 0:
        return
    
    cancelled_bookings: List[BookingSchema] = []
    for booking_id in booking_ids_to_cancel:
        booking = await db_crud.get_booking_by_id(booking_id)
        cancelled_bookings.append(booking)
        await db_crud.delete_booking_by_id(booking_id)
    
    canceled_bookings_text = "\n".join(
        TEMPLATE.CANCELLED_BOOKING.format(
            room=booking.room,
            date=booking.date,
            formatted_day_of_week=short_day_of_week(booking.date),
            timeslot=create_timeslot_str(booking.start_time, booking.end_time),
            username=booking.username,
            user_full_name=booking.user_full_name,
        ) for booking in cancelled_bookings
    )
    user_cancelled_bookings_text = TEMPLATE.USER_CANCELLED.format(user=dm.event.from_user)
    await dm.event.message.answer(
        "\n\n".join([user_cancelled_bookings_text, canceled_bookings_text])
    )

view_bookings_dialog = Dialog(
    user_bookings_window,
    on_start=on_dialog_start,
    on_close=on_dialog_close,
)
