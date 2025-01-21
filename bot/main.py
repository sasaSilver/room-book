import asyncio, dotenv, logging, locale
from aiogram import Bot, Dispatcher, executor
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, StartMode, setup_dialogs

from bot.dialogs.booking_dialog import booking_dialog, BookingDialogStates

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()
BOT_TOKEN = dotenv.get_key("../.env", "BOT_TOKEN")
properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    link_preview_is_disabled=True,
    disable_notification=True
)
bot = Bot(token=BOT_TOKEN, default=properties)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(booking_dialog)
setup_dialogs(dp)

@dp.message(Command("start"))
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        BookingDialogStates.SELECT_ROOM,
        mode=StartMode.RESET_STACK,
        data={"user": message.from_user}
    )
    await message.delete()

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    asyncio.run(dp.start_polling(bot, skip_updates=True))
