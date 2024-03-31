from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.tables import Orders
from src.backend.models import orders as orders_models
from src.backend.models import auth as auth_models
from src.backend import tables


class OrdersServices:

    async def get(self, session: AsyncSession, order_id: int):
        stmt = select(Orders).where(id=order_id)
        result: Result = await session.execute(stmt)
        order = result.scalars().all()
        return order

    async def post(self, session: AsyncSession, userdata: auth_models.User, order_data: orders_models.OrderAdd):
        new_order_data = orders_models.OrderAdd(
            name=order_data.name,
            description=order_data.description,
            user_id=userdata.id,
            status_id=2,
        )
        table_orders = tables.Orders(**new_order_data.model_dump())
        session.add(table_orders)
        await session.commit()


    async def get_all_orders(self, session: AsyncSession, limit: int = 10, offset: int = 0) -> list[
        orders_models.Orders]:
        stmt = select(Orders).limit(limit).offset(offset)
        result: Result = await session.execute(stmt)
        orders = result.scalars().all()
        return list(orders)


services = OrdersServices()
