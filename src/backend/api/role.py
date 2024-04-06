
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import role as role_models
from src.backend.models import auth as auth_models
from src.backend.services.auth import services as auth_services
from src.backend.services.role import services as role_services

router = APIRouter(tags=["Role"], prefix="/user/role")


@router.post("/")
async def change_role():
    pass


@router.get("/{role}", response_model=role_models.Role)
async def get_id_role(
        role: role_models.EnumBackendRole,
        session: AsyncSession = Depends(databaseHandler.get_session),
):
    return await role_services.get_id_role(role=role, session=session)


# user: auth_models.User = Depends(auth_services.get_current_user),

@router.get("/add/{role}")
async def add_role_in_database(
        role: role_models.EnumBackendRole,
        session: AsyncSession = Depends(databaseHandler.get_session),
):
    return await role_services.add_roles_in_database(role=role, session=session)