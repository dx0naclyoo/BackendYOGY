from src.backend.models import auth as models
from src.backend import tables
from sqlalchemy.ext.asyncio import AsyncSession


class AuthServices:
    async def get_user(self, session: AsyncSession): ...
    async def login(self): ...

    async def register(self): ...
