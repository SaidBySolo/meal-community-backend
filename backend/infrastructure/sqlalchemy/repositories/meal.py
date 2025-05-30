from datetime import date
from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.domain.entities.meal import Meal
from backend.domain.enum import CreateMealStatus
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.meal import MealSchema
from backend.infrastructure.sqlalchemy.entities.school_info import SchoolInfoSchema


class SQLAlchemyMealRepository(MealRepository):
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa

    async def _get_schema_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[MealSchema]:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(SchoolInfoSchema)
                    .where(
                        SchoolInfoSchema.edu_office_code == edu_office_code,
                        SchoolInfoSchema.standard_school_code == standard_school_code,
                    )
                    .options(
                        selectinload(
                            SchoolInfoSchema.meals.and_(MealSchema.date == date)
                        )
                    )
                )

                return [
                    meal
                    for school_info in result.scalars().all()
                    for meal in school_info.meals
                ]

    async def get_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[Meal]:
        meal_schemas = await self._get_schema_by_code(
            edu_office_code, standard_school_code, date
        )

        return [schema.to_entity() for schema in meal_schemas]

    async def get_with_id_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[tuple[int, Meal]]:
        meal_schemas = await self._get_schema_by_code(
            edu_office_code, standard_school_code, date
        )

        return [(schema.id, schema.to_entity()) for schema in meal_schemas]

    async def get_id_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        date: date,
        meal_name: Literal["조식", "중식", "석식"],
    ) -> int | None:
        async with self.sa.session_maker() as session:
            async with session.begin():
                school_info_subquery = (
                    select(SchoolInfoSchema.id)
                    .where(
                        SchoolInfoSchema.edu_office_code == edu_office_code,
                        SchoolInfoSchema.standard_school_code == standard_school_code,
                    )
                    .scalar_subquery()
                )

                result = await session.execute(
                    select(MealSchema.id).where(
                        MealSchema.school_info_id == school_info_subquery,
                        MealSchema.date == date,
                        MealSchema.name == meal_name,
                    )
                )
                return result.scalar_one_or_none()

    async def create_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ) -> CreateMealStatus | int:
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(SchoolInfoSchema.id).where(
                        SchoolInfoSchema.edu_office_code == edu_office_code,
                        SchoolInfoSchema.standard_school_code == standard_school_code,
                    )
                )

                school_info_id = result.scalar_one_or_none()
                if school_info_id is None:
                    return CreateMealStatus.SCHOOL_INFO_NOT_FOUND

                meal_schema = MealSchema(
                    school_info_id=school_info_id,
                    name=meal.name,
                    dish_name=meal.dish_name,
                    calorie=meal.calorie,
                    date=meal.date,
                    comments=[],
                )

                session.add(meal_schema)
                await session.commit()
                return meal_schema.id
