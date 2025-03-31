import datetime

from aiogram import Bot
from aiogram.types import BufferedInputFile, Message
from aiogram_dialog import DialogManager

from bot.config import settings
from bot.texts import CONST


async def send_error_report(
    message: Message,
    bot: Bot,
    data: dict,
    error_text: str,
    dialog_manager: DialogManager,
):
    bug_report = "\n".join(
        [
            f"{data['error_type']}",
            "=================",
            f"Time: {datetime.datetime.now()}",
            f"Dialog Manager: {dialog_manager.__dict__}",
            "Error:",
            f"{error_text}",
        ]
    )
    timestamp = datetime.datetime.now().strftime("%m%d_%H%M%S")
    bug_report_bytes = bug_report.encode("utf-8")
    bug_report_file = BufferedInputFile(
        file=bug_report_bytes, filename=f"error_report_{timestamp}.txt"
    )
    await bot.send_document(
        chat_id=settings.adm_id,
        document=bug_report_file,
    )
    await message.answer(CONST.ERROR_BOT)
