import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 10000
    debug: bool = False

    database_url: str = os.getenv("POSTGRES_URL")
    database_echo: bool = True

    private_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "src" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire: int = 1000000


settings = Settings()
