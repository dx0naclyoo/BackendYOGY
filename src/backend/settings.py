import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    database_url: str = os.getenv("postgres_url")
    database_echo: bool = True


settings = Settings()
