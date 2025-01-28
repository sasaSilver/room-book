import asyncio, logging, locale
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import Message, ChatMemberUpdated, User
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogManager, ShowMode, StartMode, setup_dialogs

from bot.kbd import get_main_rkeyboard as main_rkeyboard
from bot.dialogs.booking_dialog import booking_dialog, BookingDialogStates
from bot.dialogs.view_bookings_dialog import view_bookings_dialog, ViewBookingsDialogStates
from bot.settings import settings
from bot.constants import (
    CREATE_BOOKING_TEXT, MY_BOOKINGS_TEXT, WELCOME_MESSAGE
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = settings.token
properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    link_preview_is_disabled=True,
    disable_notification=True,
)
bot = Bot(token=BOT_TOKEN, default=properties)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(booking_dialog)
dp.include_router(view_bookings_dialog)
setup_dialogs(dp)

@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    user: User = message.from_user
    await message.answer(
        WELCOME_MESSAGE.format(user=user),
        reply_markup=main_rkeyboard()
    )

@dp.message(F.text.in_(["/book", CREATE_BOOKING_TEXT]))
async def make_bookingt(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        BookingDialogStates.SELECT_ROOM,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"user": message.from_user}
    )
    await message.delete()

@dp.message(F.text.in_(["/my", MY_BOOKINGS_TEXT]))
async def view_user_bookings(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        ViewBookingsDialogStates.VIEW_BOOKINGS,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={"user": message.from_user}
    )
    await message.delete()

@dp.my_chat_member()
async def on_bot_chat_member_update(event: ChatMemberUpdated):
    if event.chat.type == "private":
        return  # Only for group chats
    
    user = event.from_user
    message = await bot.send_message(
        event.chat.id,
        WELCOME_MESSAGE.format(user=user),
        reply_markup=main_rkeyboard()
    )
    await message.delete()

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    asyncio.run(dp.start_polling(bot, skip_updates=True))
