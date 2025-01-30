from aiogram import Bot
from aiogram.types import BufferedInputFile, Message
import datetime
from bot.settings import settings
    
def generate_timeslots(start_time: datetime.time, end_time: datetime.time, interval: int) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots  

def create_timeslot_str(start_time: datetime.time, end_time: datetime.time):
    start_hm: str = start_time.strftime("%H:%M")
    end_hm: str = end_time.strftime("%H:%M")
    return f"{start_hm} - {end_hm}"

async def send_error_report(message: Message, bot: Bot, data: dict, error: str):
    god_id = settings.god_id
    bug_report = (
        f"{data['error_type']} Error\n"
        f"============\n"
        f"Time: {datetime.datetime.now()}\n"
        f"User: {data['user'].username} {data['user'].full_name}, ID: {data['user'].id})\n"
        f"Room: {data['selected_room']}\n" if data.get("selected_room", False) else ""
        f"Date: {data['selected_date']}\n" if data.get("selected_date", False) else ""
        f"Time slot: {data['start_time']} - {data['end_time']}\n" if data.get("start_time", False) and data.get("end_time", False) else ""
        f"Error:\n"
        f"{error}"
    )
    timestamp = datetime.datetime.now().strftime("%m%d_%H%M%S")
    bug_report_bytes = bug_report.encode('utf-8')
    bug_report_file = BufferedInputFile(
        file=bug_report_bytes,
        filename=f"bug_report_{timestamp}.txt"
    )
    await bot.send_document(
        chat_id=god_id,
        document=bug_report_file,
    )
    await message.answer(
        
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