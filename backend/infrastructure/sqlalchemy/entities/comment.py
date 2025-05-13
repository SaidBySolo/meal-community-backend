from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.sqlalchemy.base import Base
from backend.infrastructure.sqlalchemy.entities.user import UserSchema
from backend.infrastructure.sqlalchemy.mixin import Schema


class CommentSchema(Base, Schema):
    __tablename__ = "comment"

    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    meal_id: Mapped[int] = mapped_column(ForeignKey("meal.id"))
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comment.id"), nullable=True
    )

    replies: Mapped[list[CommentSchema]] = relationship(
        "CommentSchema",
        cascade="all, delete",
    )
    author: Mapped[UserSchema] = relationship("UserSchema")

    created_at: Mapped[datetime] = mapped_column()
