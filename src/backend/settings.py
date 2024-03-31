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

    private_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire: int = 5


settings = Settings()
