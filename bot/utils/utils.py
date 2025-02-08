from enum import Enum
import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_dialog import DialogManager

from bot.texts import BTN_TEXTS
from bot.settings import settings


def get_main_rkeyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TEXTS.CREATE_BOOKING)],
            [
                KeyboardButton(text=BTN_TEXTS.MY_BOOKINGS),
                KeyboardButton(text=BTN_TEXTS.ALL_BOOKINGS),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def generate_timeslots(
    start_time: datetime.time, end_time: datetime.time, interval: int
) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time)
            + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots


def to_timeslot_str(
    start_time: datetime.time | str = None, end_time: datetime.time | str = None
):

    if not start_time or not end_time:
        return ""

    formatted = False

    if isinstance(start_time, str) and isinstance(end_time, str):
        try:
            start_time = datetime.date.fromisoformat(start_time)
            end_time = datetime.date.fromisoformat(end_time)
        except ValueError:
            formatted = True

    if not formatted:
        start_time: str = start_time.strftime("%H:%M")
        end_time: str = end_time.strftime("%H:%M")
    return f"{start_time} - {end_time}"


class TimeWindowState(Enum):
    NO_TIMESLOTS = 0
    HAS_TIMESLOTS = 1
    SELECTED_START_TIME = 2
    SELECTED_END_TIME = 3


def get_time_selection_state(dialog_manager: DialogManager):
    now = datetime.datetime.now()
    selected_timepoints = dialog_manager.find("time_selection").get_widget_data(
        dialog_manager, []
    )
    has_timeslots = now < datetime.datetime.combine(
        dialog_manager.dialog_data["selected_date"], settings.end_time
    ) - datetime.timedelta(minutes=30)
    has_start_time = len(selected_timepoints) > 0
    has_end_time = len(selected_timepoints) > 1
    # each condition satisfied "bumps up" the state of time selection window
    return TimeWindowState(has_timeslots + has_start_time + has_end_time)
