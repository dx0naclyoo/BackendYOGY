from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import auth as models
from src.backend.services.auth import services
from src.backend import tables
from src.backend.database import databaseHandler

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/", response_model=models.User)
async def user(
        userdata: models.User = Depends(services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return models.User(
        id=userdata.id,
        username=userdata.username
    )


@router.post("/login")
async def login(
        userdata: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.login(username=userdata.username, password=userdata.password, session=session)


@router.post("/register", response_model=models.Token)
async def register(
        user_data: models.UserRegister,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.register(user_data, session)
