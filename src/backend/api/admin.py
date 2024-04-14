from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.services.admin import services as admin_services

router = APIRouter(tags=["Admin"], prefix="/admin")

# user_data: models.UserRegister,
# session: AsyncSession = Depends(databaseHandler.get_session)

@router.get("/admin/projectletter/{project_id}")
async def get_letter_time_for_order(
        project_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await admin_services.get_letter_time_for_order(project_id=project_id, session=session)













