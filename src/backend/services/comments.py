from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import comments as comments_models
from src.backend import tables


class CommentsServices:
    async def add_comments_to_orders(self,
                                     comment: comments_models.Comments,
                                     order_id: int,
                                     session: AsyncSession):

        add_comment = tables.Comment(
            text=comment.text
        )

        session.add(add_comment)
        await session.commit()

        if add_comment.id:
            stmt = update(tables.Orders).where(tables.Orders.id == order_id).values(comment_id=add_comment.id)
            await session.execute(stmt)
            await session.commit()

    async def get_by_id(self, comment_id: int, session: AsyncSession):
        stmt = select(tables.Comment).where(tables.Comment.id == comment_id)
        response_db = await session.execute(stmt)
        comment = response_db.scalar()

        return comment


services = CommentsServices()
