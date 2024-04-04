from typing import Any

from fastapi import HTTPException, status

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.backend.models import auth as auth_models
from src.backend.models import orders as orders_models
from src.backend import tables


class OrdersServices:

    async def get(self,
                  session: AsyncSession,
                  user_data: auth_models.User,
                  order_id: int) -> orders_models.Orders:

        stmt = select(tables.Orders).where(tables.Orders.user_id == user_data.id and tables.Orders.id == order_id)
        result: Result = await session.execute(stmt)
        order = result.scalar()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        return orders_models.Orders.parse_obj(order)

    async def get_all(self,
                      session: AsyncSession,
                      user_data: auth_models.User,
                      limit: int = 10,
                      offset: int = 0) -> list[orders_models.Orders]:

        stmt = select(tables.Orders).where(tables.Orders.user_id == user_data.id).limit(limit).offset(offset)
        result: Result = await session.execute(stmt)
        orders = result.scalars().all()
        return list(orders)

    async def create(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     order_data: orders_models.OrderAdd):

        existing_order = await session.execute(select(tables.Orders).filter(tables.Orders.name == order_data.name))
        existing_order = existing_order.scalar()

        if existing_order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with this name already exists")

        new_order_data = orders_models.OrderAdd(
            name=order_data.name,
            description=order_data.description,
            user_id=user_data.id,
            status_id=2,
        )

        table_orders = tables.Orders(**new_order_data.model_dump())
        session.add(table_orders)
        await session.commit()
        return {"Status": "Successfully"}

    async def update(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     order_id: int,
                     order_data: orders_models.OrderUpdate,
                     ) -> orders_models.Orders:

        order = await self.get(session, order_id)

        if order.user_id != user_data.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the customer of this order")

        for name, description in order_data.dict().items():
            setattr(order, name, description)

        await session.commit()
        return orders_models.Orders(id=order.id,
                                    name=order_data.name,
                                    description=order_data.description,
                                    user_id=user_data.id)

    async def delete(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     order_id: int):

        order = await self.get(session, order_id)

        if order.user_id != user_data.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the customer of this order")

        await session.delete(order)
        await session.commit()
        return {"Status": "Successfully"}


services = OrdersServices()
