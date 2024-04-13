from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as auth_models
from src.backend.models import role as role_models
from src.backend.services.auth import services as auth_services
from src.backend.services.user import services as user_services

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/", response_model=auth_models.User)
async def get_user_by_token(
        request: Request,
        user_in_token: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    print(request.headers)
    return await user_services.get_user_by_token(user=user_in_token, session=session)


@router.get("/{id}", response_model=auth_models.User)
async def get_user_by_id(
        user_id: int,
        request: Request,
        # user_in_token: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    print(request.headers)
    return await user_services.get_user_by_id(user_id=user_id, session=session)  # user=user_in_token,


@router.get("/all/{role}", response_model=List[auth_models.User])
async def get_all_user(
        role: role_models.EnumBackendRole = role_models.EnumBackendRole.NONE,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    # print(request.headers)
    print(1)
    return await user_services.get_all_user(role=role,
                                            user=user,
                                            session=session)  # user=user_in_token,
