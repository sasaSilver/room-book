from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Row, Button, Back
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.media import MediaScroll, StaticMedia as Media

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile

import datetime

from bot import settings
from bot.utils import get_bookings_img_bytes
from bot.texts import BTN_TEXTS
import bot.database.db_op as db_op
from bot.database.schemas.booking_schema import BookingSchema

class ViewAllBookingsDialogStates(StatesGroup):
    SCHEDULE_VIEW = State()

async def dialog_init(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["date"] = datetime.date.today()

async def get_schedule_image(dialog_manager: DialogManager, **_kwargs):
    kwargs =  {
        "date": dialog_manager.dialog_data["date"],
        "rooms": settings.rooms,
        "bookings": {}
    }
    for room in settings.rooms:
        kwargs["bookings"][room] = await db_op.get_bookings_by_room(room)
    img_bytes = get_bookings_img_bytes(**kwargs)
    
    return {}

schedule_view_window = Window(
    MediaScroll(
        Media(
            
        )
    ),
    Row(
        Button(
            Const("<"),
            id="prev_week",
            on_click=None
        ),
        Button(
            Const(">"),
            id="next_week",
            on_click=None
        )
    ),
    Back(BTN_TEXTS.BACK)
    #state=ViewAllBookingsDialogStates.SCHEDULE_VIEW
)

view_all_bookings_dialog = Dialog(
    
)
