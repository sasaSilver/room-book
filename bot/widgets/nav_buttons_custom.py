from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.kbd.state import EventProcessorButton
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State
    
class SwitchToCustom(SwitchTo):
    """
    Works like a regular SwitchTo, but stores the "switching history" in dialog data.\n
    To be used in par with PreserveHistoryBack.
    """
    def __init__(
            self,
            text: Text,
            id: str,
            to_state: State,
            from_state: State
    ):
        super().__init__(
            text=text,
            id=id,
            state=to_state,
            on_click=self.create_handler(),
        )
        self.from_state = from_state
        
    def create_handler(self):
        async def add_state_to_stack(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
            if 'state_stack' not in dialog_manager.dialog_data:
                dialog_manager.dialog_data["state_stack"] = [self.from_state]
            dialog_manager.dialog_data["state_stack"].append(self.from_state)
        return add_state_to_stack


class BackCustom(EventProcessorButton):
    """
    Goes to a previous state is dialog's state stack.\n
    To be used in par with PreserveHistorySwitchTo.
    """
    def __init__(self, text: Text, id: str = "_btn_back_history_", on_click=None):
        super().__init__(text, id, on_click=self._on_click)
        
    async def _on_click(self, callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        previous_state = dialog_manager.dialog_data["state_stack"].pop()
        await dialog_manager.switch_to(previous_state)