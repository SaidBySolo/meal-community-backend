import asyncio
from datetime import timedelta

from backend.application.exceptions import MealNotFound
from backend.domain.entities.meal import Meal
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.datetime import to_date


class GetDailyMealUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def execute(
        self, edu_office_code: str, standard_school_code: str, current_date: str
    ) -> list[Meal]:
        current_datetime = to_date(current_date)

        meals = await self.meal_repository.get_by_code(
            edu_office_code, standard_school_code, current_datetime
        )

        if not meals:
            raise MealNotFound

        return meals


class GetDailyMealWithIDUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def execute(
        self, edu_office_code: str, standard_school_code: str, current_date: str
    ) -> list[tuple[int, Meal]]:
        current_datetime = to_date(current_date)

        meals_with_id = await self.meal_repository.get_with_id_by_code(
            edu_office_code, standard_school_code, current_datetime
        )

        if not meals_with_id:
            raise MealNotFound

        return meals_with_id


class GetWeeklyMealUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def execute(
        self, edu_office_code: str, standard_school_code: str, current_date: str
    ) -> list[list[Meal]]:
        current_datetime = to_date(current_date)
        dates = [
            current_datetime + timedelta(days=i)
            for i in range(-current_datetime.weekday(), 5 - current_datetime.weekday())
        ]

        nullable_meals = await asyncio.gather(
            *[
                self.meal_repository.get_by_code(
                    edu_office_code, standard_school_code, date
                )
                for date in dates
            ]
        )

        if not any(meal for meal in nullable_meals):
            raise MealNotFound

        return nullable_meals
