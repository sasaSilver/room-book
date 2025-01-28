from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from bot.constants import EMOJI_CROSS

class CustomCancel(Cancel):
    """
    Acts as a regular cancel button, but deletes the previous message as well.
    """
    def __init__(self, text=Const(EMOJI_CROSS)):
        super().__init__(text=text, on_click=self._on_click)
    
    async def _on_click(self, callback: CallbackQuery, button: Cancel, manager: DialogManager):
        await callback.message.delete()
        await manager.done()
