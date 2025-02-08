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


class MediaManager(MessageManager):
    URL_PATTERN = re.compile(r".*://(.*?)___")

    async def get_media_source(
        self,
        media: MediaAttachment,
        bot: Bot,
    ) -> Union[InputFile, str]:
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url and media.url.startswith(CONST.URL_PREFIX):
            date_iso: str = MediaManager.URL_PATTERN.search(media.url).group(1)
            date = datetime.date.fromisoformat(date_iso)
            img_bytes: bytes = get_bookings_img_bytes(
                date, settings.rooms, await db_op.get_all_bookings()
            )
            return BufferedInputFile(
                img_bytes, f"schedule_{date.strftime('%d-%m-%Y')}.png"
            )
        return await super().get_media_source(media, bot)
