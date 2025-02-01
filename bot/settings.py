from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from typing import List
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os, datetime

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=ENV_PATH)

@dataclass(frozen=True)
class Settings:    
    db_extensions: List[str]
    bot_token: str
    _db_url: str
    adm_id: int
    adm_username: str
    rooms: List[str]
    timeslot_duration: int
    start_time: datetime.time
    end_time: datetime.time

    bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
        disable_notification=True,
    )
    
    @staticmethod
    def load_from_env():
        required_env_vars = ["BOT_TOKEN", "ADM_ID", "ADM_USERNAME", "DB_URL"]
        missing_env_vars = [var for var in required_env_vars if os.getenv(var) is None]

        if missing_env_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_env_vars)}")

        return Settings(
            bot_token=os.getenv("BOT_TOKEN"),
            adm_id=int(os.getenv("ADM_ID")),
            adm_username=os.getenv("ADM_USERNAME"),
            _db_url=os.getenv("DB_URL"),
            rooms=["Аудитория А", "Аудитория В", "Аудитория С"],
            start_time=datetime.time(7, 30),
            end_time=datetime.time(18, 30),
            timeslot_duration=30,
            db_extensions=["asyncpg"]
        )

    @property
    def db_url(self) -> str:
        if not self.db_extensions:
            return self._db_url
        extensions_str = ''.join(f'+{extension}' for extension in self.db_extensions)
        return self._db_url.replace("://", f"{extensions_str}://")

settings = Settings.load_from_env()
