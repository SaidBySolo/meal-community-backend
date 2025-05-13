from abc import ABC, abstractmethod
from datetime import datetime

from backend.domain.entities.meal import Meal


class MealRepository(ABC):
    @abstractmethod
    async def get_meal_by_code(
        self, edu_office_code: str, standard_school_code: str, date: datetime
    ) -> list[Meal]: ...

    @abstractmethod
    async def create_meal_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ) -> None: ...
