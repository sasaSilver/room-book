from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_FILE)

@dataclass
class BotSettings:
    token: str = os.getenv("BOT_TOKEN")
    god_id: int = int(os.getenv("GOD_ID"))
    db_url: str = os.getenv("DB_URL").replace('postgresql://', 'postgresql+asyncpg://')

settings: BotSettings = BotSettings()

if __name__ == "__main__":
    print(settings)