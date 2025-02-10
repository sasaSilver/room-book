from typing import Dict, List

from aiogram_dialog import Dialog, DialogManager, Window, SubManager
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import ListGroup, Button, Checkbox, ManagedCheckbox

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery


from bot.utils.utils import to_timeslot_str
from bot.texts import TEMPLATES, BTNS, FORMATS
import bot.database.db_op as db_op
from bot.database.schemas.booking_schema import BookingSchema
from bot.widgets import CancelCustom, ScrollingGroupCircular


class ViewBookingsDialogStates(StatesGroup):
    VIEW_BOOKINGS = State()


async def dialog_init(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["bookings_to_cancel"] = []


def format_booking(booking: BookingSchema) -> Dict[str, str]:
    return {
        "id": booking.id,
        "room": booking.room,
        "booking_details": (
            f"{booking.date.strftime(FORMATS.DATE)} "
            f"({booking.date.strftime("%a")}) "
            f"{booking.start_time.strftime(FORMATS.TIME)}-"
            f"{booking.end_time.strftime(FORMATS.TIME)}"
        ),
    }


async def fetch_user_bookings(**kwargs):
    dm: DialogManager = kwargs["dialog_manager"]

    if formatted_bookings := dm.dialog_data.get("cached_bookings", False):
        return {
            "user": dm.event.from_user,
            "bookings": dm.dialog_data["cached_bookings"],
        }

    user_bookings = await db_op.get_bookings_by_username(dm.event.from_user.username)

    formatted_bookings = [format_booking(booking) for booking in user_bookings]
    dm.dialog_data["cached_bookings"] = formatted_bookings
    return {"user": dm.event.from_user, "bookings": formatted_bookings}


async def flag_booking_for_cancel(
    _callback: CallbackQuery, button: ManagedCheckbox, submanager: SubManager
):
    booking_id = int(submanager.item_id)
    if button.is_checked():
        submanager.manager.dialog_data["bookings_to_cancel"].append(booking_id)
    else:
        submanager.manager.dialog_data["bookings_to_cancel"].remove(booking_id)


user_bookings_window = Window(
    Case(
        {
            True: Format(TEMPLATES.USER_BOOKINGS),
            False: Format(TEMPLATES.USER_BOOKINGS_EMPTY),
        },
        selector=F["bookings"].len() > 0,
    ),
    ScrollingGroupCircular(
        ListGroup(
            Button(Format("{item[room]}"), id="booking_room"),
            Button(Format("{item[booking_details]}"), id="booking_details"),
            Checkbox(
                Const(BTNS.CANCELLED),
                Const(BTNS.CANCEL_BOOKING),
                id="btn_cancel",
                on_state_changed=flag_booking_for_cancel,
            ),
            id="user_bookings",
            items="bookings",
            item_id_getter=lambda item: item["id"],
        ),
        id="scroll_user_bookings",
        width=1,
        height=3,
        hide_on_single_page=True,
    ),
    CancelCustom(Const(BTNS.FINISH)),
    state=ViewBookingsDialogStates.VIEW_BOOKINGS,
    getter=fetch_user_bookings,
)


async def cancel_selected_bookings(_result, dm: DialogManager):
    booking_ids_to_cancel = dm.dialog_data["bookings_to_cancel"]
    if len(booking_ids_to_cancel) == 0:
        return

    cancelled_bookings: List[BookingSchema] = []
    for booking_id in booking_ids_to_cancel:
        booking = await db_op.get_booking_by_id(booking_id)
        cancelled_bookings.append(booking)
        await db_op.delete_booking_by_id(booking_id)

    canceled_bookings_text = "\n".join(
        TEMPLATES.CANCELLED_BOOKING.format(
            room=booking.room,
            date=booking.date,
            day_of_week=booking.date.strftime("%a"),
            timeslot=to_timeslot_str(booking.start_time, booking.end_time),
            username=booking.username,
            user_full_name=booking.user_full_name,
        )
        for booking in cancelled_bookings
    )
    user_cancelled_bookings_text = TEMPLATES.USER_CANCELLED.format(
        user=dm.event.from_user
    )
    await dm.event.message.answer(
        "\n\n".join([user_cancelled_bookings_text, canceled_bookings_text])
    )


view_bookings_dialog = Dialog(
    user_bookings_window,
    on_start=dialog_init,
    on_close=cancel_selected_bookings,
)
