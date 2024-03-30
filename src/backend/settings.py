from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True

    database_host: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str
