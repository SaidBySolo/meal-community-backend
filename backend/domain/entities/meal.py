from dataclasses import asdict, dataclass
from datetime import date

from backend.domain.utils import dict_factory


@dataclass
class Meal:
    name: str
    """식사명"""
    dish_name: str
    """요리명"""
    calorie: str
    """칼로리"""

    date: date
    """급식일자"""

    def to_dict(self):
        return asdict(self, dict_factory=dict_factory)
