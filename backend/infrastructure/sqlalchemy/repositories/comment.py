from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.domain.entities.comment import Comment
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.comment import CommentSchema
from backend.infrastructure.sqlalchemy.entities.user import UserSchema


class SQLAlchemyCommentRepository:
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa

    async def create_new_comment(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                author = await session.get(UserSchema, user_id)

                if not author:
                    raise ValueError("Author not found")

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

    async def create_reply(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
        parent_comment_id: int,
    ) -> bool:
        async with self.sa.session_maker() as session:
            async with session.begin():
                parent_comment = await session.get(
                    CommentSchema,
                    parent_comment_id,
                    options=[selectinload(CommentSchema.replies)],
                )

                if parent_comment is None:
                    return False

                author = await session.get(UserSchema, user_id)
                if not author:
                    raise ValueError("Author not found")

                reply = CommentSchema(
                    content=comment.content,
                    user_id=user_id,
                    meal_id=meal_id,
                    parent_id=parent_comment_id,
                    author=author,
                    replies=[],
                )

                parent_comment.replies.append(reply)

                session.add(reply)
                session.add(parent_comment)

                await session.commit()
                return True

    async def get_comments_by_meal_id(self, meal_id: int) -> list[Comment]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(CommentSchema)
                    .where(CommentSchema.meal_id == meal_id)
                    .options(selectinload(CommentSchema.replies))
                )
                comments = result.scalars().all()

                return [comment.to_entity() for comment in comments]

    async def delete_comment(self, comment_id: int) -> bool: ...

    async def update_comment_content(
        self, comment_id: int, new_content: str
    ) -> Comment: ...
