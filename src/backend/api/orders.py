from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import orders as orders_models
from src.backend.models import auth as auth_models

from src.backend.services.orders import services as orders_services
from src.backend.services.auth import services as auth_services
from src.backend.database import databaseHandler


router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/", response_model=list[orders_models.Orders])
async def get_all_products(
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await orders_services.get_all_orders(session=session)

@router.post("/")
async def post(
        order_data: orders_models.OrderAdd,
        userdata: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session),
):
    return await orders_services.post(session=session, userdata=userdata, order_data=order_data)


