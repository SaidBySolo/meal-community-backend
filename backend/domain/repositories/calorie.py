from abc import ABC, abstractmethod
from io import IOBase

from backend.domain.entities.calorie import Calorie
from backend.domain.entities.meal import Meal


class CalorieRepository(ABC):
    @abstractmethod
    async def get_calories(self, meal: Meal, image: IOBase) -> Calorie | None:
        """Retrieve the calorie count for a given food item."""
        pass
