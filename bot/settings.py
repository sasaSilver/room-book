from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)

@dataclass
class BotSettings:
    token: str = os.getenv("BOT_TOKEN")
    db_url: str = os.getenv("DB_URL").replace('postgresql://', 'postgresql+asyncpg://')
    god_id: int = int(os.getenv("GOD_ID"))

settings: BotSettings = BotSettings()

bot_properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
    link_preview_is_disabled=True,
    disable_notification=True,
)