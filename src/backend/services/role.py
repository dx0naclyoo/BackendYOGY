from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import role as role_models


class RoleServices:

    async def set_role_yourself(self,
                                user: auth_models.User,
                                session: AsyncSession,
                                new_role: role_models.EnumBackendRole) -> auth_models.User:

        old_role = await self.get_list_user_roles(user=user, session=session)

        if new_role == role_models.EnumBackendRole.ADMIN:
            if role_models.EnumBackendRole.ADMIN in old_role:
                # set role admin for user :)
                pass
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No permission for this action")

        else:
            if new_role in old_role:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already have the role")
            else:

                id_new_role = await self.get_id_role(role=new_role, session=session)

                add_role = tables.SecondaryUserRole(
                    user_id=user.id,
                    role_id=id_new_role,
                )

                session.add(add_role)
                await session.commit()

                new_roles = await self.get_list_user_roles(user=user, session=session)

                return auth_models.User(
                    username=user.username,
                    id=user.id,
                    roles=new_roles
                )

    async def add_roles_in_database(self,
                                    user: auth_models.User,
                                    role: role_models.EnumBackendRole,
                                    session: AsyncSession) -> tables.Role | None:

        roles_user = await self.get_list_user_roles(user=user, session=session)

        if role_models.EnumBackendRole.ADMIN in roles_user:
            stmt = select(tables.Role).where(tables.Role.name == role)
            db_response = await session.execute(stmt)

            if db_response.scalar():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Role with this name already exists")

            database_role = tables.Role(
                name=role
            )
            session.add(database_role)
            await session.commit()
            return database_role

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No permission for this action")

    async def get_id_role(self,
                          role: role_models.EnumBackendRole,
                          session: AsyncSession) -> int:

        stmt = select(tables.Role).where(tables.Role.name == role)
        db_response = await session.execute(stmt)
        role = db_response.scalar()

        return role.id

    async def _get_role(self,
                        role_id: int,
                        session: AsyncSession) -> tables.Role:

        stmt = select(tables.Role).where(tables.Role.id == role_id)
        db_response = await session.execute(stmt)
        role = db_response.scalar()
        return role

    async def get_list_user_roles(self,
                                  user: auth_models.User,
                                  session: AsyncSession) -> List[role_models.EnumBackendRole]:

        stmt_all = select(tables.SecondaryUserRole).where(tables.SecondaryUserRole.user_id == user.id)
        database_response = await session.execute(stmt_all)
        end_user = database_response.scalars().all()

        tables_roles_user: list[tables.Role] = \
            [await self._get_role(role_id=x.role_id, session=session) for x in end_user]

        roles_user = [x.name for x in tables_roles_user]

        return roles_user

    async def remove_role(self,
                          user: auth_models.User,
                          session: AsyncSession,
                          role: role_models.EnumBackendRole) -> auth_models.User:

        user_roles = await self.get_list_user_roles(user=user, session=session)

        if role in user_roles:
            # remove role
            id_role = await self.get_id_role(role=role, session=session)
            stmt = select(tables.SecondaryUserRole).where((tables.SecondaryUserRole.user_id == user.id)
                                                          & (tables.SecondaryUserRole.role_id == id_role))
            database_response = await session.execute(stmt)
            user_role = database_response.scalar()
            await session.delete(user_role)
            await session.commit()

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You do not have this role")

        new_user_roles = await self.get_list_user_roles(user, session)

        return auth_models.User(
            username=user.username,
            id=user.id,
            roles=new_user_roles
        )


services = RoleServices()
