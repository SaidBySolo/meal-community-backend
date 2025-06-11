from io import IOBase

from backend.application.exceptions import CalorieNotFound
from backend.domain.entities.calorie import Calorie
from backend.domain.entities.meal import Meal
from backend.domain.repositories.calorie import CalorieRepository


class GetCalorieUseCase:
    def __init__(self, calorie_repository: CalorieRepository):
        self.calorie_repository = calorie_repository

    async def execute(self, meal: Meal, image: IOBase) -> Calorie:
        calorie = await self.calorie_repository.get_calories(meal, image)
        if not calorie:
            raise CalorieNotFound
        return calorie
