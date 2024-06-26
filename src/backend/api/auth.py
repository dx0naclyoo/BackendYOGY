from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as models
from src.backend.services.auth import services

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login")
async def login(
        userdata: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    token = await services.login(username=userdata.username, password=userdata.password, session=session)

    return token


@router.post("/register")
async def register(
        user_data: models.UserRegister,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.register(user_data=user_data, session=session)
