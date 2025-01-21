from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.common.when import Predicate
from attr import s

class ShowDoneCondition(Predicate):
    def __call__(self, data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
        data = dialog_manager.dialog_data
        return data.get("time_start", False) and data.get("time_end", False)