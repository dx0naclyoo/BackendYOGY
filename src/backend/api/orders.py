from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import orders as models
from src.backend.services.orders import services

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/", response_model=list[models.Orders])
async def get_all_products(
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services.get_all_orders(session=session)
