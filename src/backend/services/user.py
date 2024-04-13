from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import role as role_models
from src.backend.services.role import services as role_services


class UserServices:
    async def get_user_by_token(self, user: auth_models.User, session: AsyncSession):
        stmt = select(tables.User).where(tables.User.id == user.id)
        result = await session.execute(stmt)
        new_user = result.scalar()

        user_roles = await role_services.get_list_user_roles_by_id_user(user_id=user.id, session=session)

        return auth_models.User(
            username=new_user.username,
            id=new_user.id,
            roles=user_roles,
        )

    async def get_user_by_id(self, user_id, session: AsyncSession):  # user: auth_models.User,
        stmt = select(tables.User).where(tables.User.id == user_id)
        result = await session.execute(stmt)
        new_user = result.scalar()

        if new_user:
            user_roles = await role_services.get_list_user_roles_by_id_user(user_id=new_user.id, session=session)

            return auth_models.User(
                username=new_user.username,
                id=new_user.id,
                roles=user_roles,
            )

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь с таким ID не найден")

    async def get_all_user(self,
                           role: role_models.EnumBackendRole,
                           user: auth_models.User,
                           session: AsyncSession) -> List[auth_models.User]:
        print(2)
        if role != role_models.EnumBackendRole.NONE:
            print(3)
            role_id = await role_services.get_id_role(role=role, session=session)

            stmt = select(tables.SecondaryUserRole).where(tables.SecondaryUserRole.role_id == role_id)
            database_response = await session.execute(stmt)
            items_user_role = database_response.scalars()

            user_list = []

            for item in items_user_role:
                database_user = await self.get_user_by_id(user_id=item.user_id, session=session)

                user_roles = await role_services.get_list_user_roles_by_id_user(user_id=database_user.id,
                                                                                session=session)

                user_list.append(auth_models.User(
                    username=database_user.username,
                    id=database_user.id,
                    roles=user_roles,
                ))
        else:
            print(4)
            stmt_all = select(tables.User)
            database_response = await session.execute(stmt_all)
            user_items = database_response.scalars()

            user_list = []

            for user_item in user_items:
                user_roles = await role_services.get_list_user_roles_by_id_user(user_id=user_item.id,
                                                                                session=session)
                user_list.append(auth_models.User(
                    username=user_item.username,
                    id=user_item.id,
                    roles=user_roles,
                ))

        return user_list


services = UserServices()
