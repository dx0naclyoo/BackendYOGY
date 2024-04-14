from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as auth_models
from src.backend.models import projects as projects_models
from src.backend.services.auth import services as auth_services
from src.backend.services.projects import services as projects_services

router = APIRouter(tags=["Projects"], prefix="/projects")


@router.get("/get/all", response_model=List[projects_models.Projects])
async def get_all(
        offset: int = 0,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await projects_services.get_all(session=session, offset=offset)


@router.get("/get/user/all", response_model=List[projects_models.Projects])
async def get_all_user_projects(
        offset: int = 0,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await projects_services.get_all_users_project(user=user, session=session, offset=offset)


@router.get("/get/lecturer", response_model=List[projects_models.Projects])
async def get_projects_lecturer(
        lecturer_id: int,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await projects_services.get_all_projects_lecturer(lecturer_id=lecturer_id, user=user, session=session)


@router.get("/get/{projects_id}")
async def get_project_by_id(
        projects_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await projects_services.get_project_by_id(projects_id=projects_id, session=session)


@router.post("/add/", response_model=projects_models.Projects)  # response_model=projects_models.Projects
async def add_projects(
        project: projects_models.AddProjects,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):

    return await projects_services.create(project=project, user=user, session=session)
