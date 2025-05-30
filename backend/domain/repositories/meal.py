from abc import ABC, abstractmethod
from datetime import date
from typing import Literal

from backend.domain.entities.meal import Meal
from backend.domain.enum import CreateMealStatus


class MealRepository(ABC):
    @abstractmethod
    async def get_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[Meal]: ...

    @abstractmethod
    async def get_with_id_by_code(
        self, edu_office_code: str, standard_school_code: str, date: date
    ) -> list[tuple[int, Meal]]: ...

    @abstractmethod
    async def create_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        meal: Meal,
    ) -> CreateMealStatus | int: ...

    @abstractmethod
    async def get_id_by_code(
        self,
        edu_office_code: str,
        standard_school_code: str,
        date: date,
        meal_name: Literal["조식", "중식", "석식"],
    ) -> int | None: ...
