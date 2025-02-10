from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const

from aiogram.fsm.state import StatesGroup, State

from bot.widgets import CancelCustom, BackCustom, SwitchToCustom
from bot.texts import BTNS, HELPS


class HelpDialogStates(StatesGroup):
    HELP_MENU = State()
    HUH_MENU = State()
    BOOK = State()
    VIEW = State()
    VIEW_ALL = State()
    CANCEL = State()
    BOT_DOWN = State()


help_window = Window(
    Const(HELPS.CHOOSE_HELP),
    SwitchToCustom(
        Const(HELPS.HOW2_MENU),
        id="btn_how2_menu",
        to_state=HelpDialogStates.HUH_MENU,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELPS.HOW2_BOOK),
        id="btn_how2_book",
        to_state=HelpDialogStates.BOOK,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELPS.HOW2_VIEW),
        id="btn_how2_view",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELPS.HOW2_VIEW_ALL),
        id="btn_how2_view_all",
        to_state=HelpDialogStates.VIEW_ALL,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELPS.HOW2_CANCEL),
        id="btn_how2_cancel",
        to_state=HelpDialogStates.CANCEL,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELPS.WHY_BOT_DOWN),
        id="btn_down_link",
        to_state=HelpDialogStates.BOT_DOWN,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    CancelCustom(),
    state=HelpDialogStates.HELP_MENU,
)

how2_menu_window = Window(
    Const(HELPS.MENU),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.HUH_MENU,
)

how2_book_window = Window(
    Const(HELPS.BOOK),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.BOOK,
)

how2_view_window = Window(
    Const(HELPS.VIEW),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.VIEW,
)

how2_viewall_window = Window(
    Const(HELPS.VIEW_ALL),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.VIEW_ALL,
)

how2_cancel_window = Window(
    Const(HELPS.CANCEL),
    SwitchToCustom(
        Const(HELPS.HOW2_VIEW),
        id="btn_how2_view_redirect",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.CANCEL,
    ),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.CANCEL,
)

why_bot_down_window = Window(
    Const(HELPS.BOT_DOWN),
    BackCustom(Const(BTNS.BACK)),
    state=HelpDialogStates.BOT_DOWN,
)

help_dialog = Dialog(
    help_window,
    how2_menu_window,
    how2_book_window,
    how2_view_window,
    how2_viewall_window,
    how2_cancel_window,
    why_bot_down_window,
)
