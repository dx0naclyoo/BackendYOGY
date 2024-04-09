from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as auth_models
from src.backend.models import orders as orders_models
from src.backend.services.orders import services as orders_services
from src.backend.services.auth import services as auth_services
from src.backend.models import projects as projects_models
from src.backend.services.projects import services as projects_services

router = APIRouter(tags=["Projects"], prefix="/projects")

@router.post("/get")
async def get_projects():
    pass


@router.post("/add/", response_model=projects_models.Projects)
async def add_projects(
        project: projects_models.AddProjects,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    pass
    # return await projects_services.create(project=project, user=user, session=session)