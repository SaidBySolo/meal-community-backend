from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.domain.entities.user import User
from backend.domain.repositories.user import UserRepository
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.school_info import SchoolInfoSchema
from backend.infrastructure.sqlalchemy.entities.user import UserSchema
from backend.infrastructure.sqlalchemy.repositories.school_info import (
    SQLAlchemySchoolInfoRepository,
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa
        self.school_info_repository = SQLAlchemySchoolInfoRepository(sa)

    async def create(self, user: User) -> User:
        async with self.sa.session_maker() as session:
            async with session.begin():
                school_info_schema = await self.school_info_repository.get_or_create(
                    SchoolInfoSchema.from_entity(user.school_info)
                )
                user_schema = UserSchema(
                    email=user.email,
                    password=user.password,
                    name=user.name,
                    grade=user.grade,
                    room=user.room,
                    school_info_id=school_info_schema.id,
                    school_info=school_info_schema,
                )
                session.add(user_schema)

            return user_schema.to_entity()

    async def get_id_by_email_with_password(
        self, email: str, password: str
    ) -> int | None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(UserSchema)
                    .where(UserSchema.email == email, UserSchema.password == password)
                    .options(selectinload(UserSchema.school_info))
                )

                user = result.scalars().first()

                if user:
                    return user.id

    async def get_by_id(self, user_id: int) -> User:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(UserSchema)
                    .where(UserSchema.id == user_id)
                    .options(selectinload(UserSchema.school_info))
                )

                user = result.scalar_one()
                return user.to_entity()

    async def get_id_by_email(self, email: str) -> int | None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(UserSchema)
                    .where(UserSchema.email == email)
                    .options(selectinload(UserSchema.school_info))
                )

                user = result.scalars().first()

                if user:
                    return user.id
