from aiogram import Bot
from aiogram.types import BufferedInputFile, Message
import datetime

from aiogram_dialog import DialogManager
from bot.settings import settings
from bot.constants import TEXT

def generate_timeslots(start_time: datetime.time, end_time: datetime.time, interval: int) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots  

def create_timeslot_str(start_time: datetime.time | str, end_time: datetime.time | str):
    if isinstance(start_time, str) and isinstance(end_time, str):
        start_time, end_time = map(datetime.time.fromisoformat, (start_time, end_time))
    start_hm: str = start_time.strftime("%H:%M")
    end_hm: str = end_time.strftime("%H:%M")
    return f"{start_hm} - {end_hm}"

async def send_error_report(message: Message, bot: Bot, data: dict, error_text: str, dialog_manager: DialogManager):
    bug_report = "\n".join([
        f"{data['error_type']}",
        f"=================",
        f"Time: {datetime.datetime.now()}",
        f"Dialog Manager: {dialog_manager.__dict__}",
        f"Error:",
        f"{error_text}"
    ])
    timestamp = datetime.datetime.now().strftime("%m%d_%H%M%S")
    bug_report_bytes = bug_report.encode("utf-8")
    bug_report_file = BufferedInputFile(
        file=bug_report_bytes,
        filename=f"error_report_{timestamp}.txt"
    )
    await bot.send_document(
        chat_id=settings.god_id,
        document=bug_report_file,
    )
    await message.answer(
        TEXT.ERROR_BOT
    )

def short_day_of_week(date: datetime.date):
    day_abbreviations = {
        "понедельник": "Пн",
        "вторник": "Вт",
        "среда": "Ср",
        "четверг": "Чт",
        "пятница": "Пт",
        "суббота": "Сб",
        "воскресенье": "Вс"
    }
    day_name = date.strftime("%A")
    abbreviated_day = day_abbreviations.get(day_name.lower(), day_name)
    return abbreviated_day