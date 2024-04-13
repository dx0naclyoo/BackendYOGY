from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import projects as projects_models
from src.backend.models import role as role_models
from src.backend.services.orders import services as order_services
from src.backend.services.role import services as role_services
from src.backend.services.user import services as user_services


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
                      user: auth_models.User,
                      limit: int = 10,
                      offset: int = 0) -> List[projects_models.Projects] | List:

        stmt = select(tables.Projects)
        database_response = await session.execute(stmt)
        projects_all = database_response.scalars()
        list_projects = []

        for x in projects_all:
            lecturer = await user_services.get_user_by_id(user_id=x.lecturer_id, session=session)
            order = await order_services.get(session=session, user_data=user, order_id=x.orders_id)

            list_projects.append(
                projects_models.Projects(
                    name=order.name,
                    description=order.description,
                    id=x.id,
                    registration_date=x.registration_date.strftime("%d.%m.%Y"),
                    count_place=x.count_place,
                    deadline_date=x.deadline_date.strftime("%d.%m.%Y"),
                    order_id=x.orders_id,
                    lecturer=lecturer,
                    customer_type=x.customer_type,
                    identity=[projects_models.EnumIdentity(x) for x in x.identity.split(" ")],
                    types=[projects_models.EnumTypes(x) for x in x.type.split(" ")],
                    spheres=[projects_models.EnumSpheres(x) for x in x.spheres.split(" ")],
                )
            )

        return list_projects

    async def get_all_projects_lecturer(self,
                                        lecturer_id: int,
                                        session: AsyncSession,
                                        user: auth_models.User, ):

        stmt = select(tables.Projects).where(tables.Projects.lecturer_id == lecturer_id)
        database_response = await session.execute(stmt)
        projects_all = database_response.scalars()
        list_projects = []

        for x in projects_all:
            lecturer = await user_services.get_user_by_id(user_id=x.lecturer_id, session=session)
            order = await order_services.get(session=session, user_data=user, order_id=x.orders_id)

            list_projects.append(
                projects_models.Projects(
                    name=order.name,
                    description=order.description,
                    id=x.id,
                    registration_date=x.registration_date.strftime("%d.%m.%Y"),
                    count_place=x.count_place,
                    deadline_date=x.deadline_date.strftime("%d.%m.%Y"),
                    order_id=x.orders_id,
                    lecturer=lecturer,
                    customer_type=x.customer_type,
                    identity=[projects_models.EnumIdentity(x) for x in x.identity.split(" ")],
                    types=[projects_models.EnumTypes(x) for x in x.type.split(" ")],
                    spheres=[projects_models.EnumSpheres(x) for x in x.spheres.split(" ")],
                )
            )
        return list_projects

    async def create(self,
                     session: AsyncSession,
                     user: auth_models.User,
                     project: projects_models.AddProjects) -> projects_models.Projects:

        user_role = await role_services.get_list_user_roles_by_id_user(user_id=user.id, session=session)

        if role_models.EnumBackendRole.ADMIN in user_role:
            new_project = tables.Projects(
                count_place=project.count_place,
                deadline_date=project.deadline_date,
                orders_id=project.order_id,
                lecturer_id=project.lecturer_id,
                customer_type=project.customer_type,

                identity=" ".join(project.identity),
                type=" ".join(project.types),
                spheres=" ".join(project.spheres),
            )

            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)

            lecturer = await user_services.get_user_by_id(user_id=new_project.lecturer_id, session=session)
            order = await order_services.get(session=session, user_data=user, order_id=new_project.orders_id)

            return projects_models.Projects(
                name=order.name,
                description=order.description,
                id=new_project.id,
                registration_date=new_project.registration_date,
                count_place=new_project.count_place,
                deadline_date=new_project.deadline_date,
                order_id=new_project.orders_id,
                lecturer=lecturer,
                customer_type=new_project.customer_type,
                identity=[projects_models.EnumIdentity(x) for x in new_project.identity.split(" ")],
                types=[projects_models.EnumTypes(x) for x in new_project.type.split(" ")],
                spheres=[projects_models.EnumSpheres(x) for x in new_project.spheres.split(" ")],
            )

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only Admins can create projects")

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
