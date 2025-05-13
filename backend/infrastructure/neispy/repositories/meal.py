from datetime import datetime

from neispy import Neispy
from neispy.error import DataNotFound

from backend.domain.entities.meal import Meal
from backend.domain.repositories.meal import MealRepository
from backend.infrastructure.datetime import to_yyyymmdd
from backend.infrastructure.neispy.entities.meal import NeispyMeal


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

        return [NeispyMeal.from_neispy(meal) for meal in row]

    async def create_meal_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ) -> None:
        raise NotImplementedError(
            "Cannot create meal with NeispyMealRepository. Use SQLAlchemyMealRepository instead."
        )
