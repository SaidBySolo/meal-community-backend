from datetime import date
from typing import Literal

from neispy import Neispy
from neispy.error import DataNotFound

from backend.domain.entities.meal import Meal
from backend.domain.enum import CreateMealStatus
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.datetime import to_yyyymmdd
from backend.infrastructure.neispy.entities.meal import NeispyMeal


class NeispyMealRepository(MealRepository):
    def __init__(self, neispy: Neispy):
        self.neispy = neispy

    async def get_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[Meal]:

        try:
            info = await self.neispy.mealServiceDietInfo(
                ATPT_OFCDC_SC_CODE=edu_office_code,
                SD_SCHUL_CODE=standard_school_code,
                MLSV_YMD=to_yyyymmdd(date),
            )
        except DataNotFound:
            return []

        row = info.mealServiceDietInfo[1].row

        return [NeispyMeal.from_neispy(meal) for meal in row]

    async def get_with_id_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[tuple[int, Meal]]:
        raise NotImplementedError("Cannot get meal with id with NeispyMealRepository.")

    async def get_id_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        date: date,
        meal_name: Literal["조식", "중식", "석식"],
    ) -> int | None:
        raise NotImplementedError("Cannot get meal id with NeispyMealRepository.")

    async def create_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ) -> CreateMealStatus:
        raise NotImplementedError("Cannot create meal with NeispyMealRepository.")
    
    async def get_by_id(self, meal_id: int) -> Meal:
        raise NotImplementedError("Cannot get meal by id with NeispyMealRepository.")
