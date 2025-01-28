import asyncio, logging, locale
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, StartMode, setup_dialogs

from bot.dialogs.booking_dialog import booking_dialog, BookingDialogStates
from bot.dialogs.view_bookings_route import view_bookings_dialog, ViewBookingsDialogStates
from bot.settings import settings

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

@dp.message(F.text.in_(["/start", "Создать бронь"]))
async def make_bookingt(message: Message, dialog_manager: DialogManager):
    await message.delete()
    await dialog_manager.start(
        BookingDialogStates.SELECT_ROOM,
        mode=StartMode.RESET_STACK,
        data={"user": message.from_user}
    )

@dp.message(F.text.in_(["/my", "Мои бронирования"]))
async def view_user_bookings(message: Message, dialog_manager: DialogManager):
    await message.delete()
    await dialog_manager.start(
        ViewBookingsDialogStates.VIEW_BOOKINGS,
        mode=StartMode.RESET_STACK,
        data={"user": message.from_user}
    )

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    asyncio.run(dp.start_polling(bot, skip_updates=True))
