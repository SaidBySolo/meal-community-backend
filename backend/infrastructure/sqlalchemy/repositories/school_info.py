from sqlalchemy import and_, select

from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.school_info import SchoolInfoSchema


class SQLAlchemySchoolInfoRepository:
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa

    async def get_or_create(
        self, school_info_schema: SchoolInfoSchema
    ) -> SchoolInfoSchema:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(SchoolInfoSchema).where(
                    and_(
                        SchoolInfoSchema.edu_office_code
                        == school_info_schema.edu_office_code,
                        SchoolInfoSchema.standard_school_code
                        == school_info_schema.standard_school_code,
                    )
                )
            )
            schema = result.scalars().first()

            if schema:
                return schema

            session.add(school_info_schema)

        return school_info_schema

    async def get_by_code(
        self, edu_office_code: str, standard_school_code: str
    ) -> SchoolInfoSchema | None:
        async with self.sa.session_maker() as session:
            result = await session.execute(
                select(SchoolInfoSchema).where(
                    and_(
                        SchoolInfoSchema.edu_office_code == edu_office_code,
                        SchoolInfoSchema.standard_school_code == standard_school_code,
                    )
                )
            )

            return result.scalars().first()
