from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.entities.user import User
from backend.infrastructure.sqlalchemy.base import Base
from backend.infrastructure.sqlalchemy.entities.school_info import SchoolInfoSchema
from backend.infrastructure.sqlalchemy.mixin import Schema


class UserSchema(Base, Schema):
    __tablename__ = "user"
    name: Mapped[str] = mapped_column()
    """이름"""
    email: Mapped[str] = mapped_column()
    """이메일"""
    password: Mapped[str] = mapped_column()
    """비밀번호"""
    school_info_id: Mapped[int] = mapped_column(ForeignKey("school_info.id"))
    """학교 정보 ID"""
    school_info: Mapped[SchoolInfoSchema] = relationship(
        uselist=False,
        lazy="selectin",
    )
    """학교 정보"""
    grade: Mapped[int] = mapped_column()
    room: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    """생성일"""

    def to_entity(self) -> User:
        user = User(
            name=self.name,
            email=self.email,
            password=self.password,
            school_info=self.school_info.to_entity(),
            grade=self.grade,
            room=self.room,
        )
        user.created_at = self.created_at
        return user

    @classmethod
    def from_entity(cls, user: User, school_info_id: int) -> UserSchema:
        return cls(
            name=user.name,
            email=user.email,
            password=user.password,
            school_info_id=school_info_id,
            school_info=SchoolInfoSchema.from_entity(user.school_info),
            grade=user.grade,
            room=user.room,
            created_at=user.created_at,
        )
