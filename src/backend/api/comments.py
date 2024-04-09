from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.services.comments import services as comment_services
from src.backend.models import comments as comment_models

router = APIRouter(tags=["OrderComments"], prefix="/comments")


@router.post("/add")
async def add_comments(
        comment: comment_models.Comments,
        order_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await comment_services.add_comments_to_orders(comment=comment, order_id=order_id, session=session)
