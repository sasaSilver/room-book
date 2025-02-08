from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile, BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.message_manager import MessageManager
from aiogram_dialog.api.entities import MediaAttachment

from enum import Enum
import datetime
from typing import Union

from bot.texts import BTN_TEXTS, settings
from bot.settings import settings
from bot.utils.booking_img_bytes import get_bookings_img_bytes

def get_main_rkeyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_TEXTS.CREATE_BOOKING),
                KeyboardButton(text=BTN_TEXTS.MY_BOOKINGS),
                KeyboardButton(text=BTN_TEXTS.ALL_BOOKINGS)
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )

def generate_timeslots(
        start_time: datetime.time,
        end_time: datetime.time,
        interval: int
) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots  

def create_timeslot_str(start_time: datetime.time | str, end_time: datetime.time | str):
    if isinstance(start_time, str):
        start_time = datetime.date.fromisoformat(start_time)
        
    if isinstance(end_time, str):
        end_time = datetime.date.fromisoformat(end_time)
        
    start_hm: str = start_time.strftime("%H:%M")
    end_hm: str = end_time.strftime("%H:%M")
    return f"{start_hm} - {end_hm}"

def get_timeslot_text(dm: DialogManager):
    selected_times = dm.find("time_selection").get_widget_data(dm, [])
    if len(selected_times) < 2:
        return None
    return '-'.join(selected_times)

class TimeWindowState(Enum):
    NO_TIMESLOTS = 0
    HAS_TIMESLOTS = 1
    SELECTED_START_TIME = 2
    SELECTED_END_TIME = 3

def get_time_selection_state(dialog_manager: DialogManager):
    now = datetime.datetime.now()
    selected_timepoints = dialog_manager.find("time_selection").get_widget_data(dialog_manager, [])
    has_timeslots = now < datetime.datetime.combine(
        dialog_manager.dialog_data["selected_date"], settings.end_time
    ) - datetime.timedelta(minutes=30)
    has_start_time = len(selected_timepoints) > 0
    has_end_time = len(selected_timepoints) > 1
    # each condition satisfied "bumps up" the state of time selection window
    return TimeWindowState(has_timeslots + has_start_time + has_end_time)

class MessageManagerMedia(MessageManager):
    async def get_media_source(
        self, media: MediaAttachment, bot: Bot,
    ) -> Union[InputFile, str]:
        URL_PREFIX = "my://"
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url and media.url.startswith(URL_PREFIX):
            img_bytes = media.url[len(URL_PREFIX):]
            return BufferedInputFile(img_bytes, f"schedule.png")
        return await super().get_media_source(media, bot)
