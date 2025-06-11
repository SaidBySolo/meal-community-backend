from dataclasses import asdict, dataclass


@dataclass
class Menu:
    name: str
    calories: int | None = None


@dataclass
class Calorie:
    meals: list[Menu]
    total_calories: int | None = None

    def to_dict(self):
        return asdict(self)