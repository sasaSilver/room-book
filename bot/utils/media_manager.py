import re
import datetime
from typing import Union

from aiogram import Bot
from aiogram.types import InputFile, BufferedInputFile
from aiogram_dialog.manager.message_manager import MessageManager
from aiogram_dialog.api.entities import MediaAttachment

from bot.utils.booking_img_bytes import get_bookings_img_bytes
import bot.database.db_op as db_op
from bot.settings import settings
from bot.texts import CONST

SCHEDULE_URL_RE = re.compile(CONST.SCHEDULE_URL_PATTERN)

class MediaManager(MessageManager):
    async def get_media_source(
        self,
        media: MediaAttachment,
        bot: Bot,
    ) -> Union[InputFile, str]:
        if media.file_id or not(media.url and media.url.startswith(CONST.URL_PREFIX)):
            return await super().get_media_source(media, bot)
        date_iso: str = SCHEDULE_URL_RE.search(media.url).group(1)
        date = datetime.date.fromisoformat(date_iso)
        img_bytes: bytes = get_bookings_img_bytes(
            date, settings.rooms, await db_op.get_all_bookings()
        )
        return BufferedInputFile(
            img_bytes, f"schedule_{date.strftime('%d-%m-%Y')}.png"
        )
        
