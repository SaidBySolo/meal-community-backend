from datetime import datetime
from neispy import Neispy

from backend.domain.entities.meal import Meal
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.neispy.entities.meal import NeispyMeal
from backend.infrastructure.datetime import to_yyyymmdd
from neispy.error import DataNotFound


class NeispyMealRepository(MealRepository):
    def __init__(self, neispy: Neispy):
        self.neispy = neispy

    async def get_meal_by_code(
        self, edu_office_code: str, standard_school_code: str, date: datetime
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

        return [
            NeispyMeal.from_neispy(meal)
            for meal in row
        ]
