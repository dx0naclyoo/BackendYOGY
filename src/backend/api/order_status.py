
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import order_status as models_order_status
from src.backend.services.auth import services as auth_services
from src.backend.models import auth as auth_models
from src.backend.database import databaseHandler
from src.backend.services.order_status import services as services_order_status
from src.backend.models import orders as models_orders

router = APIRouter(tags=["OrderStatus"], prefix="/order_status")


@router.get("/add/{data}", response_model=models_order_status.OrderStatus)
async def add_order_status_id_database(
        data: models_order_status.EnumOrderStatis,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)
):
    return await services_order_status.add_to_database(data=data, user=user, session=session)


@router.post("/set/{order_id}")
async def set_status_for_orders(
        order_id: int,
        status_order: models_order_status.EnumOrderStatis,
        user: auth_models.User = Depends(auth_services.get_current_user),
        session: AsyncSession = Depends(databaseHandler.get_session)):

    return await services_order_status.set_status_for_orders(status_order=status_order,
                                                             order_id=order_id,
                                                             user=user,
                                                             session=session)
