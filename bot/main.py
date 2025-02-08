import asyncio, logging, locale
from aiogram import Bot, Dispatcher, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ChatMemberUpdated, ErrorEvent
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogManager, ShowMode, StartMode, setup_dialogs
from aiogram_dialog.api.exceptions import DialogsError, UnknownIntent

from bot.routers.user.create_booking import booking_dialog, BookingDialogStates
from bot.routers.user.user_bookings import view_bookings_dialog, ViewBookingsDialogStates
from bot.routers.user.help import help_dialog, HelpDialogStates
from bot.routers.user.all_bookings import view_all_bookings_dialog, ViewAllBookingsDialogStates
from bot.settings import settings
from bot.texts import BTN_TEXTS, TEMPLATES
from bot.utils import send_error_report, get_main_rkeyboard

async def start(message: Message):
    await message.answer(
        TEMPLATES.REGISTERED_USER.format(user=message.from_user),
        reply_markup=get_main_rkeyboard()
    )
    await message.delete()

async def create_booking(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        BookingDialogStates.SELECT_ROOM,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        data={"user": message.from_user}
    )
    await message.delete()

async def view_user_bookings(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        ViewBookingsDialogStates.VIEW_BOOKINGS,
        mode=StartMode.NEW_STACK,
        show_mode=ShowMode.EDIT,
    )
    await message.delete()

async def view_all_bookings(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        ViewAllBookingsDialogStates.SELECT_VIEW,
        mode=StartMode.NEW_STACK,
        show_mode=ShowMode.EDIT
    )
    await message.delete()

async def register_new_user(event: ChatMemberUpdated):
    if event.chat.type == "private":
        return
    
    user = event.from_user
    message = await bot.send_message(
        event.chat.id,
        TEMPLATES.REGISTERED_USER.format(user=user),
        reply_markup=get_main_rkeyboard()
    )
    await message.delete()

async def help_user(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        HelpDialogStates.HELP_MENU,
        mode=StartMode.NEW_STACK,
        show_mode=ShowMode.EDIT
    )
    await message.delete()

async def error_handler(event: ErrorEvent, message: Message, bot: Bot, dialog_manager: DialogManager):
    error = event.exception
    error_type = error.__class__.__name__
    logging.error(f"{error_type}: {event.exception}")
    error_data = {
        "message": message,
        "bot": bot,
        "data": {"error_type": error_type, "dialog_manager": dialog_manager},
        "dialog_manager": dialog_manager,
        "error_text": None
    }
    if isinstance(error, ConnectionResetError):
        error_data["error_text"] = f"Database not responding:\n{str(error)}"
    else:
        error_data["error_text"] = str(error)
    await send_error_report(**error_data)
    
def setup_dp():
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.register(start, F.text == "/start")
    dp.message.register(create_booking, F.text.in_(["/book", BTN_TEXTS.CREATE_BOOKING]))
    dp.message.register(view_user_bookings, F.text.in_(["/my", BTN_TEXTS.MY_BOOKINGS]))
    dp.message.register(help_user, F.text.in_(["/help"]))
    #dp.message.register(view_all_bookings, F.text.in_(["/all", BTN_TEXTS.ALL_BOOKINGS]))
    dp.my_chat_member.register(register_new_user, F.update.bot.as_("bot"))
    dp.errors.register(
        error_handler,
        ExceptionTypeFilter(Exception, UnknownIntent, DialogsError),
        F.update.message.as_("message"),
        F.update.bot.as_("bot")
    )
    
    dp.include_router(booking_dialog)
    dp.include_router(view_bookings_dialog)
    dp.include_router(help_dialog)
    dp.include_router(view_all_bookings_dialog)
    setup_dialogs(dp)
    
    return dp
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    locale.setlocale(locale.LC_ALL, '') # for local date and time formatting, 'LC_ALL' just in case

    bot = Bot(token=settings.bot_token, default=settings.bot_properties)
    dp = setup_dp()
    
    asyncio.run(dp.start_polling(
        bot,
        skip_updates=True,
        close_bot_session=True,
        handle_signals=True
    ))