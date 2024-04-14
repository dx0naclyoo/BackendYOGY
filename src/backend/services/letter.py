from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.services.user import services as user_services
from src.backend.models import letter as letter_models
from src.backend.models import auth as auth_models

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
                text=item.text,
                user=user
            ))

        return list_letters


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
            text=new_letter.text,
            user=user
        )

services = ServicesLetter()
