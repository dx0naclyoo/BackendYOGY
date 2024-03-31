from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as models


class AuthServices:
    async def get_user(self, user_id, session: AsyncSession):
        return user_id

    async def login(self, session: AsyncSession):
        ...

    async def register(self, user_data: models.UserRegister, session: AsyncSession):

        stmt = select(tables.User).where(tables.User.username == user_data.username)
        db_response = await session.execute(stmt)
        db_user = db_response.scalar()

        if db_user is None:
            user = tables.User(
                username=user_data.username,
                password=user_data.password
            )
            session.add(user)
            await session.commit()

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Users already exist",
                headers={
                    "WWW-Authenticate": 'Bearer'
                }
            )


services = AuthServices()
