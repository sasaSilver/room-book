from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const

from aiogram.fsm.state import StatesGroup, State

from bot.widgets import CustomCancel, Previous, SwitchToSavePrevious
from bot.constants import BTN_TEXT, HELP_TEXT

class HelpDialogStates(StatesGroup):
    HELP_MENU = State()
    HUH_MENU = State()
    BOOK = State()
    VIEW = State()
    VIEW_ALL = State()
    CANCEL = State()

help_window = Window(
    Const(HELP_TEXT.CHOOSE_HELP),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_MENU),
        id="btn_how2_menu",
        to_state=HelpDialogStates.HUH_MENU,
        from_state=HelpDialogStates.HELP_MENU
    ),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_BOOK),
        id="btn_how2_book",
        to_state=HelpDialogStates.BOOK,
        from_state=HelpDialogStates.HELP_MENU
    ),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_VIEW),
        id="btn_how2_view",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.HELP_MENU
    ),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_VIEW_ALL),
        id="btn_how2_view_all",
        to_state=HelpDialogStates.VIEW_ALL,
        from_state=HelpDialogStates.HELP_MENU
    ),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_CANCEL),
        id="btn_how2_cancel",
        to_state=HelpDialogStates.CANCEL,
        from_state=HelpDialogStates.HELP_MENU
    ),
    CustomCancel(),
    state=HelpDialogStates.HELP_MENU
)

how2_menu_window = Window(
    Const(HELP_TEXT.MENU),
    Previous(Const(BTN_TEXT.BACK)),
    state=HelpDialogStates.HUH_MENU
)

how2_book_window = Window(
    Const(HELP_TEXT.BOOK),
    Previous(Const(BTN_TEXT.BACK)),
    state=HelpDialogStates.BOOK
)

how2_view_window = Window(
    Const(HELP_TEXT.VIEW),
    Previous(Const(BTN_TEXT.BACK)),
    state=HelpDialogStates.VIEW
)

how2_viewall_window = Window(
    Const(HELP_TEXT.VIEW_ALL),
    Previous(Const(BTN_TEXT.BACK)),
    state=HelpDialogStates.VIEW_ALL
)

how2_cancel_window = Window (
    Const(HELP_TEXT.CANCEL),
    SwitchToSavePrevious(
        Const(HELP_TEXT.HOW2_VIEW),
        id="btn_how2_view_redirect",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.CANCEL
    ),
    Previous(Const(BTN_TEXT.BACK)),
    state=HelpDialogStates.CANCEL
)

help_dialog = Dialog(
    help_window,
    how2_menu_window,
    how2_book_window,
    how2_view_window,
    how2_viewall_window,
    how2_cancel_window,
)