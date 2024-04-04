from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as auth_models
from src.backend.models import orders as orders_models
from src.backend.services.orders import services as orders_services
from src.backend.services.auth import services as auth_services

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/all/{offset}", response_model=list[orders_models.Orders])
async def get_orders_all(
        offset: int,
        session: AsyncSession = Depends(databaseHandler.get_session),
        user_data: auth_models.User = Depends(auth_services.get_current_user),
):
    return await orders_services.get_all(session=session, offset=offset, user_data=user_data)


@router.get("/{order_id}", response_model=orders_models.Orders)
async def get_order(
        order_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session),
        user_data: auth_models.User = Depends(auth_services.get_current_user),
):
    return await orders_services.get(session=session, order_id=order_id, user_data=user_data)


@router.post("/")
async def create_order(
        order_data: orders_models.OrderAdd,
        session: AsyncSession = Depends(databaseHandler.get_session),
        user_data: auth_models.User = Depends(auth_services.get_current_user),
):
    return await orders_services.create(session=session, user_data=user_data, order_data=order_data)


@router.put("/{id}", response_model=orders_models.Orders)
async def update_order(
        order_id: int,
        order_data: orders_models.OrderUpdate,
        session: AsyncSession = Depends(databaseHandler.get_session),
        user_data: auth_models.User = Depends(auth_services.get_current_user),
):
    return await orders_services.update(session=session, user_data=user_data, order_id=order_id, order_data=order_data)


@router.delete("/{order_id}")
async def delete_order(
        order_id: int,
        session: AsyncSession = Depends(databaseHandler.get_session),
        user_data: auth_models.User = Depends(auth_services.get_current_user),
):
    return await orders_services.delete(session=session, user_data=user_data, order_id=order_id)
