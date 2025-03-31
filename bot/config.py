import datetime

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import LinkPreviewOptions


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", enable_decoding=False)
    
    bot_token: str
    db_uri: str
    adm_id: int
    adm_username: str
    rooms: list[str]
    sql_echo: bool = False
    timeslot_duration: int = 30
    start_time: datetime.time = datetime.time(7, 30)
    end_time: datetime.time = datetime.time(18, 30)
    
    bot_properties: DefaultBotProperties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview=LinkPreviewOptions(is_disabled=True),
        disable_notification=True,
    )
    
    @field_validator('rooms', mode='before')
    def parse_rooms(cls, v: str):
        return v.split(',')

Settings.model_rebuild()
settings = Settings()
