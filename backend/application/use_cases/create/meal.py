from backend.application.exceptions import SchoolNotFound
from backend.domain.entities.meal import Meal
from backend.domain.enum import CreateMealStatus
from backend.domain.repositories.meal import MealRepository


class CreateMealUseCase:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def execute(
        self, edu_office_code: str, standard_school_code: str, meal: Meal
    ) -> None:
        result = await self.meal_repository.create_by_code(
            edu_office_code=edu_office_code,
            standard_school_code=standard_school_code,
            meal=meal,
        )

        if result == CreateMealStatus.SCHOOL_INFO_NOT_FOUND:
            raise SchoolNotFound

        return
