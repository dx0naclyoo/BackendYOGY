from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.services.comments import services as comment_services
from src.backend.models import comments as comment_models
from src.backend.models import auth as auth_models
from src.backend.services.auth import services as auth_services

router = APIRouter(tags=["OrderComments"], prefix="/comments")


@router.post("/add")
async def add_comments(
        comment: comment_models.Comments,
        order_id: int,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await comment_services.add_comments_to_orders(user=user, comment=comment, order_id=order_id, session=session)
