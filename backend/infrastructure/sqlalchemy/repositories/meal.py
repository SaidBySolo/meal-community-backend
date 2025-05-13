from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.domain.entities.meal import Meal
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.entities.meal import MealSchema
from backend.infrastructure.sqlalchemy.entities.school_info import SchoolInfoSchema


class SQLAlchemyMealRepository(MealRepository):
    def __init__(self, sa: SQLAlchemy):
        self.sa = sa

    async def get_meal_by_code(
        self, edu_office_code: str, standard_school_code: str, date: datetime
    ) -> list[Meal]:
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
                    meal.to_entity()
                    for school_info in result.scalars().all()
                    for meal in school_info.meals
                ]

    async def create_meal_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ):
        async with self.sa.session_maker() as session:
            async with session.begin():
                result = await session.execute(
                    select(SchoolInfoSchema).where(
                        SchoolInfoSchema.edu_office_code == edu_office_code,
                        SchoolInfoSchema.standard_school_code == standard_school_code,
                    )
                )

                school_info = result.scalars().first()
                assert school_info is not None

                meal_schema = MealSchema(
                    school_info_id=school_info.id,
                    name=meal.name,
                    dish_name=meal.dish_name,
                    calorie=meal.calorie,
                    date=meal.date,
                    comments=[],
                )

                session.add(meal_schema)
                await session.commit()
