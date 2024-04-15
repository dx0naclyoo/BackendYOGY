from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import letter as letter_models
from src.backend.services.user import services as user_services
from src.backend.models import role as role_models


class ServicesLetter:
    async def get_letter_for_order(self,
                                   project_id: int,
                                   session: AsyncSession
                                   ):
        stmt = select(tables.MotivationLetters).where(tables.MotivationLetters.projects_id == project_id)
        db_result = await session.execute(stmt)
        letters = db_result.scalars()

        list_letters = []
        for item in letters:
            user = await user_services.get_user_by_id(user_id=item.user_id, session=session)
            list_letters.append(letter_models.Letter(
                id=item.id,
                text=item.text,
                user=user,
                project_id=item.projects_id
            ))

        return list_letters

    async def get_letter_by_id(self,
                               letter_id: int,
                               session: AsyncSession
                               ):
        stmt = select(tables.MotivationLetters).where(tables.MotivationLetters.id == letter_id)
        result = await session.execute(stmt)
        letter = result.scalar()

        if letter:
            user = await user_services.get_user_by_id(user_id=letter.user_id, session=session)

            return letter_models.Letter(
                id=letter.id,
                text=letter.text,
                user=user,
                project_id=letter.projects_id
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Letter not found")

    async def add_letter(self,
                         letter: letter_models.AddLetter,
                         project_id: int,
                         user: auth_models.User,
                         session: AsyncSession
                         ):

        new_letter = tables.MotivationLetters(
            text=letter.text,
            user_id=user.id,
            projects_id=project_id
        )

        session.add(new_letter)
        await session.commit()

        await session.refresh(new_letter)

        return letter_models.Letter(
            id=new_letter.id,
            text=new_letter.text,
            user=user,
            project_id=new_letter.projects_id
        )

    async def delete_letter(self, letter_id: int, session: AsyncSession):
        letter = await self.get_letter_by_id(letter_id=letter_id, session=session)
        if not letter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

        await session.delete(letter)
        await session.commit()
        return {"Status": "Successfully"}


services = ServicesLetter()
