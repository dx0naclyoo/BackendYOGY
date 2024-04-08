from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import projects as projects_models


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
                     user: auth_models.User,
                     project: projects_models.AddProjects) -> projects_models.Projects:
        new_project = tables.Projects(
            count_place=project.count_place,
            deadline_date=project.deadline_date,
            customer_type=project.customer_type,
            orders_id=project.orders_id,
            lecturer_id=project.lecturer_id
        )

        session.add(new_project)
        await session.commit()

        await session.refresh(new_project)

        return projects_models.Projects(
            count_place=new_project.count_place,
            deadline_date=new_project.deadline_date,
            customer_type=new_project.customer_type,
            orders_id=new_project.orders_id,
            lecturer_id=new_project.lecturer_id,
            id=new_project.id,
            registration_date=new_project.registration_date
        )

    # async def update(self,
    #                  session: AsyncSession,
    #                  user_data: auth_models.User,
    #                  project_id: int,
    #                  project_data: orders_models.OrderUpdate,
    #                  ):
    #
    #     pass
    #
    # async def delete(self,
    #                  session: AsyncSession,
    #                  user_data: auth_models.User,
    #                  project_id: int):
    #     pass


services = ProjectsServices()
