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
from src.backend.services.letter import services as letter_services
from src.backend.models import letter as letter_models

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
                      limit: int = 10,
                      offset: int = 0) -> List[projects_models.Projects] | List:

        stmt = select(tables.Projects).offset(offset).limit(limit)
        database_response = await session.execute(stmt)
        projects_all = database_response.scalars()
        list_projects = []

        for x in projects_all:
            lecturer = await user_services.get_user_by_id(user_id=x.lecturer_id, session=session)
            order = await order_services.get_by_id(session=session, order_id=x.orders_id)
            students = await self.get_binding_students_for_project(project_id=x.id, session=session)

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
                    students=students,
                    customer_type=x.customer_type,
                    identity=[projects_models.EnumIdentity(x) for x in x.identity.split(" ")],
                    types=[projects_models.EnumTypes(x) for x in x.type.split(" ")],
                    spheres=[projects_models.EnumSpheres(x) for x in x.spheres.split(" ")],
                )
            )

        return list_projects

    async def get_all_users_project(self,
                                    session: AsyncSession,
                                    user: auth_models.User,
                                    limit: int = 10,
                                    offset: int = 0) -> List[projects_models.Projects] | List:

        stmt = select(tables.Projects).offset(offset).limit(limit)
        database_response = await session.execute(stmt)
        projects_all = database_response.scalars()
        list_projects = []

        for x in projects_all:
            lecturer = await user_services.get_user_by_id(user_id=x.lecturer_id, session=session)
            order = await order_services.get(session=session, user_data=user, order_id=x.orders_id)
            students = await self.get_binding_students_for_project(project_id=x.id, session=session)

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
                    students=students,
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
            students = await self.get_binding_students_for_project(project_id=x.id, session=session)

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
                    students=students,
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
            students = await self.get_binding_students_for_project(project_id=new_project.id, session=session)

            return projects_models.Projects(
                name=order.name,
                description=order.description,
                id=new_project.id,
                registration_date=new_project.registration_date,
                count_place=new_project.count_place,
                deadline_date=new_project.deadline_date,
                order_id=new_project.orders_id,
                lecturer=lecturer,
                students=students,
                customer_type=new_project.customer_type,
                identity=[projects_models.EnumIdentity(x) for x in new_project.identity.split(" ")],
                types=[projects_models.EnumTypes(x) for x in new_project.type.split(" ")],
                spheres=[projects_models.EnumSpheres(x) for x in new_project.spheres.split(" ")],
            )

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only Admins can create projects")

    async def get_project_by_id(self, projects_id, session: AsyncSession) -> projects_models.Projects:
        stmt = select(tables.Projects).where(tables.Projects.id == projects_id)
        response_database = await session.execute(stmt)
        database_project = response_database.scalar()

        if database_project:
            lecturer = await user_services.get_user_by_id(user_id=database_project.lecturer_id, session=session)
            order = await order_services.get_by_id(session=session, order_id=database_project.orders_id)
            students = await self.get_binding_students_for_project(project_id=projects_id, session=session)
            return projects_models.Projects(
                name=order.name,
                description=order.description,
                id=database_project.id,
                registration_date=database_project.registration_date,
                count_place=database_project.count_place,
                deadline_date=database_project.deadline_date,
                order_id=database_project.orders_id,
                lecturer=lecturer,
                students=students,
                customer_type=database_project.customer_type,
                identity=[projects_models.EnumIdentity(x) for x in database_project.identity.split(" ")],
                types=[projects_models.EnumTypes(x) for x in database_project.type.split(" ")],
                spheres=[projects_models.EnumSpheres(x) for x in database_project.spheres.split(" ")],
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


    async def get_numb_student_in_project(self, project_id: int, session: AsyncSession):
        stmt = select(tables.SecondaryProjectUser).where(tables.SecondaryProjectUser.projects_id == project_id)
        result = await session.execute(stmt)
        students = result.scalars()

        numb = 0
        if students:
            for _ in students:
                numb += 1

        return numb

    async def check_binding_student_in_project(self, project_id: int,student_id: int, session: AsyncSession):
        stmt = select(tables.SecondaryProjectUser).where(tables.SecondaryProjectUser.user_id == student_id)
        result = await session.execute(stmt)
        items = result.scalars()

        for x in items:
            if x.projects_id == project_id:
                return True

        return False

    async def get_binding_students_for_project(self, project_id: int, session: AsyncSession):
        stmt = select(tables.SecondaryProjectUser).where(tables.SecondaryProjectUser.projects_id == project_id)
        db_response = await session.execute(stmt)
        students = db_response.scalars()

        list_students = []

        for student in students:
            stud = await user_services.get_user_by_id(user_id=student.user_id, session=session)
            list_students.append(stud)

        return list_students

    async def accept_student_in_project(self,
                                        letter_id: int,
                                        session: AsyncSession,
                                        user: auth_models.User):

        letter = await letter_services.get_letter_by_id(letter_id=letter_id, session=session)
        project = await self.get_project_by_id(letter.project_id, session)
        numb_students = await self.get_numb_student_in_project(project_id=letter.project_id, session=session)

        if project.lecturer.id == user.id:

            if not await self.check_binding_student_in_project(letter.project_id, letter.user.id, session):

                if project.count_place > numb_students:
                    new_elem = tables.SecondaryProjectUser(
                        user_id=letter.user.id,
                        projects_id=letter.project_id
                    )

                    session.add(new_elem)
                    await session.commit()

                    await letter_services.delete_letter(letter_id=letter.id, session=session)

                    return {"response": 200, "status": "Successful"}
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Кол-во мест недостаточно для добавления нового студента")

            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already binding")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Только Руководитель проекта может это делать")

    async def reject_student_in_project(self,
                                        student_id: int,
                                        project_id: int,
                                        session: AsyncSession,
                                        user: auth_models.User):
        pass


services = ProjectsServices()
