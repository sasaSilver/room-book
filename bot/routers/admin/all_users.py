from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from aiogram.fsm.state import State, StatesGroup

class ManageAdminsStates(StatesGroup):
    CHOOSE_ACTION = State()