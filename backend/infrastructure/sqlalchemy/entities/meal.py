from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.meal import Meal
from backend.infrastructure.sqlalchemy.base import Base
from backend.infrastructure.sqlalchemy.entities.comment import CommentSchema
from backend.infrastructure.sqlalchemy.mixin import Schema


class MealSchema(Base, Schema):
    __tablename__ = "meal"

    school_info_id: Mapped[int] = mapped_column(
        ForeignKey("school_info.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column()
    """식사명"""
    dish_name: Mapped[str] = mapped_column()
    """요리명"""
    calorie: Mapped[str] = mapped_column()
    """칼로리"""

    date: Mapped[datetime] = mapped_column()
    """급식일자"""

    comments: Mapped[list[CommentSchema]] = relationship(
        "CommentSchema",
        cascade="all, delete",
        passive_deletes=True,
        collection_class=list,
    )

    def to_entity(self) -> Meal:
        return Meal(
            name=self.name,
            dish_name=self.dish_name,
            calorie=self.calorie,
            date=self.date,
        )
