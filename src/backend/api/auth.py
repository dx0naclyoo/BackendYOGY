from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import auth as models
from src.backend.services.auth import services
from src.backend import tables
from src.backend.database import databaseHandler

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/{user_id}")
async def user(
        user_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.get_user(user_id, session)


@router.post("/login")
async def login():
    return await services.login()


@router.post("/register")
async def register(
        user_data: models.UserRegister,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.register(user_data, session)
