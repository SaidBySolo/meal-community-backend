from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.comment import Comment
from backend.infrastructure.sqlalchemy.base import Base
from backend.infrastructure.sqlalchemy.entities.user import UserSchema
from backend.infrastructure.sqlalchemy.mixin import Schema


class CommentSchema(Base, Schema):
    __tablename__ = "comment"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    meal_id: Mapped[int] = mapped_column(ForeignKey("meal.id"))

    content: Mapped[str]

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comment.id"), nullable=True
    )

    replies: Mapped[list[CommentSchema]] = relationship(
        "CommentSchema",
        cascade="all, delete",
        remote_side=[parent_id],
        lazy="selectin",
    )
    author: Mapped[UserSchema] = relationship(
        "UserSchema", uselist=False, lazy="selectin"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def to_entity(self) -> Comment:
        comment = Comment(
            content=self.content,
            author=self.author.to_entity(),
            parent_id=self.parent_id,
            replies=[reply.to_entity() for reply in self.replies],
        )
        comment.created_at = self.created_at
        comment.id = self.id
        return comment
