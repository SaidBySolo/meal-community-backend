from dataclasses import dataclass


@dataclass
class Menu:
    name: str
    calories: int | None = None


@dataclass
class Calorie:
    meals: list[Menu]
    total_calories: int | None = None

    