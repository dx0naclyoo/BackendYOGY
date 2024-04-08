from typing import Any

from fastapi import HTTPException, status

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.backend.models import auth as auth_models
from src.backend.models import projects as projects_models
from src.backend import tables


class ProjectsServices:

    async def _get(self, session: AsyncSession, project_id: int):
        pass

    async def get(self,
                  session: AsyncSession,
                  user_data: auth_models.User,
                  project_id: int):
        pass



    async def get_all(self,
                      session: AsyncSession,
                      user_data: auth_models.User,
                      limit: int = 10,
                      offset: int = 0):
        pass

    async def create(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     project_data: orders_models.OrderAddForUSER):
        pass

    async def update(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     project_id: int,
                     project_data: orders_models.OrderUpdate,
                     ):

        pass

    async def delete(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     project_id: int):
        pass


services = ProjectsServices()
