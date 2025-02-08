import os
import datetime
import re
from typing import List
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
REQUIRED_ENV = ["DB_URL", "BOT_TOKEN", "ADM_ID", "ADM_USERNAME", "ROOMS"]

load_dotenv(dotenv_path=ENV_PATH)


def validate_env():
    missing_env_vars = [var for var in REQUIRED_ENV if os.getenv(var) is None]
    if missing_env_vars:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing_env_vars)}"
        )
    rooms = os.getenv("ROOMS")
    rooms_pattern = re.compile(r'^[^,]+(,[^,]+)*$')
    if not rooms_pattern.match(rooms):
        raise ValueError(
            "Invalid format for ROOMS environment variable."
            f"Expected pattern: '<room_1>,<room_2>,<room_n>', but got: '{rooms}'"
        )


@dataclass(frozen=True)
class Settings:
    bot_token: str
    db_url: str
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
        validate_env()
        return Settings(
            bot_token=os.getenv("BOT_TOKEN"),
            adm_id=int(os.getenv("ADM_ID")),
            adm_username=os.getenv("ADM_USERNAME"),
            db_url=os.getenv("DB_URL"),
            rooms=os.getenv("ROOMS").split(','),
            start_time=datetime.time(7, 30),
            end_time=datetime.time(18, 30),
            timeslot_duration=30,
        )


settings = Settings.load_from_env()
