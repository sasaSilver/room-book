import asyncio, logging, locale
from aiogram import Bot, Dispatcher, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ChatMemberUpdated, User, ErrorEvent
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogManager, ShowMode, StartMode, setup_dialogs
from aiogram_dialog.api.exceptions import DialogsError

from bot.kbd import get_main_rkeyboard as main_rkeyboard
from bot.routers.user.booking_dialog import booking_dialog, BookingDialogStates
from bot.routers.user.view_bookings_dialog import view_bookings_dialog, ViewBookingsDialogStates
from bot.settings import settings, bot_properties
from bot.constants import BTN_TEXT, TEMPLATE
from bot.utils import send_error_report

async def start(message: Message):
    await message.answer(
        TEMPLATE.REGISTERED_USER.format(user=message.from_user),
        reply_markup=main_rkeyboard()
    )

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
        data={"user": message.from_user}
    )
    await message.delete()

async def on_bot_chat_member_update(event: ChatMemberUpdated):
    if event.chat.type == "private":
        return
    
    user = event.from_user
    message = await bot.send_message(
        event.chat.id,
        TEMPLATE.REGISTERED_USER.format(user=user),
        reply_markup=main_rkeyboard()
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
        "error_text": None
    }
    if isinstance(error, ConnectionResetError):
        error_data["error"] = f"Database not responding:\n{str(error)}"
    else:
        error_data["error"] = str(error)
    await send_error_report(**error_data)
    
def setup_dp():
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.register(start, F.text == "/start")
    dp.message.register(create_booking, F.text.in_(["/book", BTN_TEXT.CREATE_BOOKING]))
    dp.message.register(view_user_bookings, F.text.in_(["/my", BTN_TEXT.MY_BOOKINGS]))
    dp.my_chat_member.register(on_bot_chat_member_update, F.update.bot.as_("bot"))
    dp.errors.register(
        error_handler,
        F.update.message.as_("message"),
        F.update.bot.as_("bot")
    )
    dp.include_router(booking_dialog)
    dp.include_router(view_bookings_dialog)
    setup_dialogs(dp)
    
    return dp
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    locale.setlocale(locale.LC_ALL, '') # for local date and time formatting, 'LC_ALL' just in case

    bot = Bot(token=settings.token, default=bot_properties)
    dp = setup_dp()
    
    asyncio.run(dp.start_polling(
        bot,
        skip_updates=True,
        close_bot_session=True,
        handle_signals=True
    ))