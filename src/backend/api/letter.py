from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import letter as letter_models
from src.backend.services.letter import services as letter_services
from src.backend.services.auth import services as auth_services
from src.backend.models import auth as auth_models

router = APIRouter(tags=["ProjectLetter"], prefix="/letter")

# user: auth_models.User = Depends(auth_services.get_current_user),
# session: AsyncSession = Depends(databaseHandler.get_session)


@router.get("/all/{project_id}", response_model=List[letter_models.Letter])
async def get_letter_for_order(
        project_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)):
    return await letter_services.get_letter_for_order(project_id=project_id, session=session)


@router.get("/{letter_id}", response_model=letter_models.Letter)
async def get_letter_by_id(
        letter_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)):
    return await letter_services.get_letter_by_id(letter_id=letter_id, session=session)


@router.post("/add/{project_id}")
async def add_letter(
        letter: letter_models.AddLetter,
        project_id: int,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)):
    return await letter_services.add_letter(letter=letter,
                                            project_id=project_id,
                                            user=user,
                                            session=session)


# @router.delete("/delete")
# async def delete_letter(letter: letter_models.DeleteLetter):
#     pass
