from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as auth_models
from src.backend.models import order_status as models_order_status
from src.backend.models import orders as models_orders


class ServicesOrderStatus:

    async def get_by_name(self,
                          name: models_order_status.EnumOrderStatis,
                          session: AsyncSession) -> tables.OrderStatus:
        stmt = select(tables.OrderStatus).where(tables.OrderStatus.name == name)
        database_response = await session.execute(stmt)
        tables_order_status = database_response.scalar()

        return tables_order_status

    async def get_by_id(self,
                        order_id: int,
                        session: AsyncSession) -> tables.OrderStatus:
        stmt = select(tables.OrderStatus).where(tables.OrderStatus.id == order_id)
        database_response = await session.execute(stmt)
        tables_order_status = database_response.scalar()
        return tables_order_status

    async def get_status_for_orders(self,
                                    order_id,
                                    session: AsyncSession):
        pass

    async def add_to_database(self,
                              data: models_order_status.EnumOrderStatis,
                              user: auth_models.User,
                              session: AsyncSession
                              ):

        role = await self.get_by_name(name=data, session=session)

        if role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status already exists")

        else:
            new_order_status = tables.OrderStatus(
                name=data
            )

            session.add(new_order_status)
            await session.commit()

            return models_order_status.OrderStatus(
                id=new_order_status.id,
                name=new_order_status.name
            )

    async def set_status_for_orders(self,
                                    status_order: models_order_status.EnumOrderStatis,
                                    order_id: int,
                                    user: auth_models.User,
                                    session: AsyncSession):

        stmt = select(tables.Orders).where(tables.Orders.id == order_id)
        resp = await session.execute(stmt)
        order = resp.scalar()
        print("ORDER", order)

        if order.user_id == user.id:
            new_status = await self.get_by_name(name=status_order, session=session)
            print("В if else")

            update_stmt = update(tables.Orders).where(tables.Orders.id == order_id).values(status_id=new_status.id)
            await session.execute(update_stmt)
            await session.commit()

            return models_orders.Orders(
                id=order.id,
                name=order.name,
                description=order.description,
                user_id=order.user_id,
                status=models_order_status.OrderStatus(
                    id=new_status.id,
                    name=new_status.name
                )
            )

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нет прав на это действие")


services = ServicesOrderStatus()
