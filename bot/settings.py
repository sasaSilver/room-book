from dataclasses import dataclass
import os

@dataclass
class BotSettings:
    token: str = os.getenv("BOT_TOKEN")
    god_id: int = int(os.getenv("GOD_ID"))
    db_url: str = os.getenv("DB_URL")

settings = BotSettings()
