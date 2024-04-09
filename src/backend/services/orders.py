from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import order_status as order_status_models
from src.backend.models import orders as orders_models
from src.backend.services.order_status import services as order_status_services


class OrdersServices:

    async def _get(self, session: AsyncSession, order_id: int) -> tables.Orders:
        stmt = select(tables.Orders).where(tables.Orders.id == order_id)
        result: Result = await session.execute(stmt)
        order = result.scalar()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        return order

    async def get(self,
                  session: AsyncSession,
                  user_data: auth_models.User,
                  order_id: int) -> orders_models.Orders:

        stmt = select(tables.Orders).where((tables.Orders.user_id == user_data.id) & (tables.Orders.id == order_id))
        result: Result = await session.execute(stmt)
        order = result.scalar()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        order_status = await order_status_services.get_by_id(order_id=order.status_id, session=session)

        return orders_models.Orders(
            id=order.id,
            name=order.name,
            description=order.description,
            user_id=order.user_id,
            status=order_status_models.OrderStatus(
                id=order_status.id,
                name=order_status.name
            )
        )

    async def get_all(self,
                      session: AsyncSession,
                      user_data: auth_models.User,
                      limit: int = 10,
                      offset: int = 0) -> list[orders_models.Orders]:

        stmt = select(tables.Orders).where(tables.Orders.user_id == user_data.id).limit(limit).offset(offset)
        result: Result = await session.execute(stmt)
        orders = result.scalars().all()

        new_order_list = []
        for x in orders:
            order_status = await order_status_services.get_by_id(order_id=x.status_id, session=session)
            new_order_list.append(
                orders_models.Orders(
                    id=x.id,
                    name=x.name,
                    description=x.description,
                    user_id=x.user_id,
                    status=order_status_models.OrderStatus(
                        id=order_status.id,
                        name=order_status.name
                    )
                )
            )

        return list(new_order_list)

    async def create(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     order_data: orders_models.OrderAddForUSER):

        database_response = await session.execute(select(tables.Orders).filter(tables.Orders.name == order_data.name))
        existing_order = database_response.scalar()

        if existing_order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with this name already exists")

        stmt_undef_role = select(tables.OrderStatus).where(
            tables.OrderStatus.name == order_status_models.EnumOrderStatis.Processing)
        resp = await session.execute(stmt_undef_role)
        processing_status = resp.scalar()

        if processing_status:
            new_order_data = orders_models.OrderAddForBackend(
                name=order_data.name,
                description=order_data.description,
                user_id=user_data.id,
                status_id=processing_status.id,
            )

            table_orders = tables.Orders(**new_order_data.model_dump())
            session.add(table_orders)
            await session.commit()
            return {"Status": "Successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось получить роль статуса")

    async def update(self,
                     session: AsyncSession,
                     user_data: auth_models.User,
                     order_id: int,
                     order_data: orders_models.OrderUpdate,
                     ) -> orders_models.Orders:

        order = await self._get(session=session, order_id=order_id)

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

        order = await self._get(session=session, order_id=order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

        if order.user_id != user_data.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the customer of this order")

        await session.delete(order)
        await session.commit()
        return {"Status": "Successfully"}


services = OrdersServices()
