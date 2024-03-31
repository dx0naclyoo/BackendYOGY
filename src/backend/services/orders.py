from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import orders as models


async def get_all_orders(session: AsyncSession, limit: int = 10, offset: int = 0) -> list[models.Orders]:
    stmt = select(models.Orders).limit(limit).offset(offset)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)
