from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.domain.entities.comment import Comment
from backend.domain.enum import CreateCommentStatus
from backend.domain.repositories.comment import CommentRepository
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.comment import CommentSchema
from backend.infrastructure.sqlalchemy.entities.user import UserSchema


class SQLAlchemyCommentRepository(CommentRepository):
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa

    async def create_new(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> CreateCommentStatus:
        async with self.sa.session_maker() as session:
            async with session.begin():
                author = await session.get(UserSchema, user_id)

                if not author:
                    return CreateCommentStatus.AUTHOR_NOT_FOUND

                comment_schema = CommentSchema(
                    content=comment.content,
                    user_id=user_id,
                    meal_id=meal_id,
                    parent_id=None,
                    author=author,
                    replies=[],
                )
                session.add(comment_schema)

                await session.commit()
                return CreateCommentStatus.SUCCESS

    async def create_reply(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> CreateCommentStatus:
        async with self.sa.session_maker() as session:
            async with session.begin():
                parent_comment = await session.get(
                    CommentSchema,
                    comment.parent_id,
                    options=[selectinload(CommentSchema.replies)],
                )

                if parent_comment is None:
                    return CreateCommentStatus.PARENT_COMMENT_NOT_FOUND

                author = await session.get(UserSchema, user_id)
                if author is None:
                    return CreateCommentStatus.AUTHOR_NOT_FOUND

                reply = CommentSchema(
                    content=comment.content,
                    user_id=user_id,
                    meal_id=meal_id,
                    parent_id=parent_comment.id,
                    author=author,
                    replies=[],
                )

                parent_comment.replies.append(reply)

                session.add(parent_comment)

                await session.commit()
                return CreateCommentStatus.SUCCESS

    async def get_by_meal_id(self, meal_id: int) -> list[Comment]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(CommentSchema)
                    .where(CommentSchema.meal_id == meal_id)
                    .options(selectinload(CommentSchema.replies))
                )
                comments = result.scalars().all()

                return [
                    comment.to_entity()
                    for comment in comments
                    if comment.parent_id is None
                ]

    async def delete(self, comment_id: int) -> bool:
        async with self.sa.session_maker() as session:
            async with session.begin():
                comment = await session.get(CommentSchema, comment_id)

                if not comment:
                    return False

                await session.delete(comment)
                await session.commit()
                return True

    async def update_content(self, comment_id: int, content: str) -> Comment | None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                comment = await session.get(CommentSchema, comment_id)

                if not comment:
                    return None

                comment.content = content
                await session.commit()
                return comment.to_entity()
