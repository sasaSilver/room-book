from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.common.when import Predicate
import datetime

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