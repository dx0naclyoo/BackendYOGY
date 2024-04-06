from fastapi import Depends, HTTPException, status
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import role as role_models


class RoleServices:

    async def set_role(self, session: AsyncSession, user: auth_models.User):
        pass

    async def add_roles_in_database(self, role: role_models.EnumBackendRole, session: AsyncSession):

        stmt = select(tables.Role).where(tables.Role.name == role)
        db_response = await session.execute(stmt)

        if db_response.scalar():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role with this name already exists")

        database_role = tables.Role(
            name=role
        )
        print(database_role)
        session.add(database_role)
        await session.commit()

    async def get_id_role(self, role: role_models.EnumBackendRole, session: AsyncSession):
        stmt = select(tables.Role).where(tables.Role.name == role)
        db_response = await session.execute(stmt)
        role = db_response.scalar()

        return role_models.Role(
            id=role.id,
            name=role.name
        )

    async def get_role(self, role_id: int, session: AsyncSession) -> tables.Role:
        stmt = select(tables.Role).where(tables.Role.id == role_id)
        db_response = await session.execute(stmt)
        role = db_response.scalar()
        return role


services = RoleServices()
