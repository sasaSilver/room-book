from tracemalloc import start
from aiogram import Bot
from aiogram.types import BufferedInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.common.when import Predicate
import datetime, os
from bot.settings import settings

class ShowDoneCondition(Predicate):
    def __call__(self, data: dict, _widget: Whenable, dialog_manager: DialogManager) -> bool:
        data = dialog_manager.dialog_data
        return data.get("time_start", False) and data.get("time_end", False)


def generate_timeslots(start_time: datetime.time, end_time: datetime.time, interval: int) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots  

def create_timeslot_str(start_iso: str, end_iso: str):
    start_hm: str = datetime.time.fromisoformat(start_iso).strftime("%H:%M")
    end_hm: str = datetime.time.fromisoformat(end_iso).strftime("%H:%M")
    return f"{start_hm} - {end_hm}"

async def send_error_report(bot: Bot, data: dict, error: str):
    god_id = settings.god_id
    bug_report = (
        f"API Error\n"
        f"============\n"
        f"Time: {datetime.datetime.now()}\n"
        f"User: {data['user'].username} {data['user'].full_name}, ID: {data['user'].id})\n"
        f"Room: {data['selected_room']}\n"
        f"Date: {data['selected_date']}\n"
        f"Time slot: {data['time_start']} - {data['time_end']}\n"
        f"Error:\n{error}\n"
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
        caption="<b><i>Booking API Error</i></b>"
    )
    if os.path.exists(f"bug_report_{timestamp}.txt"):
        os.remove(f"bug_report_{timestamp}.txt")
