from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import databaseHandler
from backend.models import auth as models
from backend.services.auth import services

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/", response_model=models.User)
async def user(
        userdata: models.User = Depends(services.get_current_user),
):
    return models.User(
        id=userdata.id,
        username=userdata.username
    )


@router.post("/login", response_model=models.Token)
async def login(
        response: Response,
        userdata: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    token = await services.login(username=userdata.username, password=userdata.password, session=session)
    # response.headers["Authorization"] = f"{token.token_type} {token.access_token}"
    return token


@router.post("/register", response_model=models.Token)
async def register(
        user_data: models.UserRegister,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.register(user_data=user_data, session=session)
