import datetime
from typing import Any
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery


from bot.texts import BTN_TEXTS
from bot.widgets.cancel_custom_ import CancelCustom


class ViewAllBookingsDialogStates(StatesGroup):
    SCHEDULE_VIEW = State()


async def dialog_init(_callback: CallbackQuery, dialog_manager: DialogManager):
    dialog_manager.dialog_data["date"] = datetime.date.today()


async def get_schedule_image(dialog_manager: DialogManager, **_kwargs):
    date: datetime.date = dialog_manager.dialog_data["date"]

    return {"date_iso": date.isoformat(), "salt": dialog_manager.current_context().id}


async def next_day(_callback: CallbackQuery, _button: Any, dm: DialogManager):
    date = dm.dialog_data["date"]
    date = (
        datetime.datetime.combine(date, datetime.time(0, 0))
        + datetime.timedelta(days=1)
    ).date()
    dm.dialog_data["date"] = date


async def prev_day(_callback: CallbackQuery, _button: Any, dm: DialogManager):
    date = dm.dialog_data["date"]
    date = (
        datetime.datetime.combine(date, datetime.time(0, 0))
        - datetime.timedelta(days=1)
    ).date()
    dm.dialog_data["date"] = date


schedule_view_window = Window(
    StaticMedia(
        url=Format("schedule://{date_iso}___{salt}"),
        use_pipe=True
    ),
    Row(
        Button(
            Const(" "),
            id="_",
            when=F["dialog_data"]["date"] <= datetime.date.today()
        ),
        Button(
            Const("<"),
            id="prev_day",
            on_click=prev_day,
            when=F["dialog_data"]["date"] > datetime.date.today(),
        ),
        Button(
            Const(">"),
            id="next_day",
            on_click=next_day
        ),
    ),
    CancelCustom(Const(BTN_TEXTS.CLOSE)),
    getter=get_schedule_image,
    state=ViewAllBookingsDialogStates.SCHEDULE_VIEW,
)

view_all_bookings_dialog = Dialog(schedule_view_window, on_start=dialog_init)
