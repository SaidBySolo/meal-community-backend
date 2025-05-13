from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    """생성일"""
    school_info: Mapped[SchoolInfoSchema] = relationship(
        uselist=False, cascade="all, delete", passive_deletes=True, default=None
    )
    """학교 정보"""

    def to_entity(self) -> User:
        return User(
            name=self.name,
            email=self.email,
            password=self.password,
            school_info=self.school_info.to_entity(),
            created_at=self.created_at,
        )

    @classmethod
    def from_entity(cls, user: User) -> UserSchema:
        return cls(
            name=user.name,
            email=user.email,
            password=user.password,
            school_info=SchoolInfoSchema.from_entity(user.school_info),
            created_at=user.created_at,
        )
