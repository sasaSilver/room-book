from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const

from aiogram.fsm.state import StatesGroup, State

from bot.widgets import CancelCustom, BackCustom, SwitchToCustom
from bot.texts import BTN_TEXTS, HELP_TEXTS


class HelpDialogStates(StatesGroup):
    HELP_MENU = State()
    HUH_MENU = State()
    BOOK = State()
    VIEW = State()
    VIEW_ALL = State()
    CANCEL = State()
    BOT_DOWN = State()


help_window = Window(
    Const(HELP_TEXTS.CHOOSE_HELP),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_MENU),
        id="btn_how2_menu",
        to_state=HelpDialogStates.HUH_MENU,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_BOOK),
        id="btn_how2_book",
        to_state=HelpDialogStates.BOOK,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_VIEW),
        id="btn_how2_view",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_VIEW_ALL),
        id="btn_how2_view_all",
        to_state=HelpDialogStates.VIEW_ALL,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_CANCEL),
        id="btn_how2_cancel",
        to_state=HelpDialogStates.CANCEL,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    SwitchToCustom(
        Const(HELP_TEXTS.WHY_BOT_DOWN),
        id="btn_down_link",
        to_state=HelpDialogStates.BOT_DOWN,
        from_state=HelpDialogStates.HELP_MENU,
    ),
    CancelCustom(),
    state=HelpDialogStates.HELP_MENU,
)

how2_menu_window = Window(
    Const(HELP_TEXTS.MENU),
    BackCustom(Const(BTN_TEXTS.BACK)),
    state=HelpDialogStates.HUH_MENU,
)

how2_book_window = Window(
    Const(HELP_TEXTS.BOOK),
    BackCustom(Const(BTN_TEXTS.BACK)),
    state=HelpDialogStates.BOOK,
)

how2_view_window = Window(
    Const(HELP_TEXTS.VIEW),
    BackCustom(Const(BTN_TEXTS.BACK)),
    state=HelpDialogStates.VIEW,
)

how2_viewall_window = Window(
    Const(HELP_TEXTS.VIEW_ALL),
    BackCustom(Const(BTN_TEXTS.BACK)),
    state=HelpDialogStates.VIEW_ALL,
)

how2_cancel_window = Window(
    Const(HELP_TEXTS.CANCEL),
    SwitchToCustom(
        Const(HELP_TEXTS.HOW2_VIEW),
        id="btn_how2_view_redirect",
        to_state=HelpDialogStates.VIEW,
        from_state=HelpDialogStates.CANCEL,
    ),
    BackCustom(Const(BTN_TEXTS.BACK)),
    state=HelpDialogStates.CANCEL,
)

why_bot_down_window = Window(
    Const(HELP_TEXTS.BOT_DOWN),
    BackCustom(Const(BTN_TEXTS.BACK)),
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
