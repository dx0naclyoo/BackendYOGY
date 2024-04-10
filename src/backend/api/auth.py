from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as models
from src.backend.services.auth import services

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/", response_model=models.User)
async def user(
        request: Request,
        # user_in_token: models.User = Depends(services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    print(request.headers)
    pass
    # return await services.get_user(user=user_in_token, session=session)


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
