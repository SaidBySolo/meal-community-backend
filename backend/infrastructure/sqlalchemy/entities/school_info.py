from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.school_info import SchoolInfo
from backend.infrastructure.sqlalchemy.base import Base
from backend.infrastructure.sqlalchemy.mixin import Schema

if TYPE_CHECKING:
    from backend.infrastructure.sqlalchemy.entities.meal import MealSchema


class SchoolInfoSchema(Base, Schema):
    __tablename__ = "school_info"
    """
    학교정보 스키마입니다.
    """

    name: Mapped[str] = mapped_column()
    grade: Mapped[int] = mapped_column()
    room: Mapped[int] = mapped_column()

    edu_office_code: Mapped[str] = mapped_column()
    standard_school_code: Mapped[str] = mapped_column()

    meals: Mapped[list[MealSchema]] = relationship(
        "MealSchema",
        cascade="all, delete",
        passive_deletes=True,
    )
    """급식정보"""

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        default=None,
        unique=True,
    )

    def to_entity(self) -> SchoolInfo:
        return SchoolInfo(
            name=self.name,
            grade=self.grade,
            room=self.room,
            edu_office_code=self.edu_office_code,
            standard_school_code=self.standard_school_code,
        )

    @classmethod
    def from_entity(cls, school_info: SchoolInfo) -> SchoolInfoSchema:
        return cls(
            name=school_info.name,
            grade=school_info.grade,
            room=school_info.room,
            edu_office_code=school_info.edu_office_code,
            standard_school_code=school_info.standard_school_code,
            meals=[],
        )
