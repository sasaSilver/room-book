from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Back, Button
from aiogram_dialog.widgets.text import Const

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from bot.widgets.custom_cancel_widget import CustomCancel
from bot.constants import BTN_TEXT, HELP_TEXT

class HelpDialogStates(StatesGroup):
    HELP_MENU = State()
    HUH_MENU = State()
    BOOK = State()
    VIEW = State()
    VIEW_ALL = State()
    CANCEL = State()

async def init_state_stack(start_data: dict, dialog_manager: DialogManager):
    dialog_manager.dialog_data["state_stack"] = []

def create_handler_for_state(state: State):
    async def add_state_to_stack(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.dialog_data["state_stack"].append(state)
    return add_state_to_stack

async def goto_previous_state(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    previous_state = dialog_manager.dialog_data["state_stack"].pop()
    await dialog_manager.switch_to(previous_state)    

BTN_BACK = Button(
    Const(BTN_TEXT.BACK),
    id="btn_back",
    on_click=goto_previous_state
)

help_window = Window(
    Const(HELP_TEXT.CHOOSE_HELP),
    SwitchTo(
        Const(HELP_TEXT.HOW2_MENU),
        id="bt2_how2_menu",
        state=HelpDialogStates.HUH_MENU,
        on_click=create_handler_for_state(HelpDialogStates.HELP_MENU)
    ),
    SwitchTo(
        Const(HELP_TEXT.HOW2_BOOK),
        id="btn_how2_book",
        state=HelpDialogStates.BOOK,
        on_click=create_handler_for_state(HelpDialogStates.HELP_MENU)
    ),
    SwitchTo(
        Const(HELP_TEXT.HOW2_VIEW),
        id="btn_how2_view",
        state=HelpDialogStates.VIEW,
        on_click=create_handler_for_state(HelpDialogStates.HELP_MENU)
    ),
    SwitchTo(
        Const(HELP_TEXT.HOW2_VIEW_ALL),
        id="btn_how2_view_all",
        state=HelpDialogStates.VIEW_ALL,
        on_click=create_handler_for_state(HelpDialogStates.HELP_MENU)
    ),
    SwitchTo(
        Const(HELP_TEXT.HOW2_CANCEL),
        id="btn_how2_cancel",
        state=HelpDialogStates.CANCEL,
        on_click=create_handler_for_state(HelpDialogStates.HELP_MENU)
    ),
    CustomCancel(),
    state=HelpDialogStates.HELP_MENU
)

how2_menu_window = Window(
    Const(HELP_TEXT.MENU),
    BTN_BACK,
    state=HelpDialogStates.HUH_MENU
)

how2_book_window = Window(
    Const(HELP_TEXT.BOOK),
    BTN_BACK,
    state=HelpDialogStates.BOOK
)

how2_view_window = Window(
    Const(HELP_TEXT.VIEW),
    BTN_BACK,
    state=HelpDialogStates.VIEW
)

how2_viewall_window = Window(
    Const(HELP_TEXT.VIEW_ALL),
    BTN_BACK,
    state=HelpDialogStates.VIEW_ALL
)

how2_cancel_window = Window (
    Const(HELP_TEXT.CANCEL),
    SwitchTo(
        Const(HELP_TEXT.HOW2_VIEW),
        id="btn_how2_view_redirect",
        state=HelpDialogStates.VIEW,
        on_click=create_handler_for_state(HelpDialogStates.CANCEL)
    ),
    BTN_BACK,
    state=HelpDialogStates.CANCEL
)

help_dialog = Dialog(
    help_window,
    how2_menu_window,
    how2_book_window,
    how2_view_window,
    how2_viewall_window,
    how2_cancel_window,
    on_start=init_state_stack
)