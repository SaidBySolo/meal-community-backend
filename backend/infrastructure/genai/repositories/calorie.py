from io import IOBase
from json import loads

from google.genai.client import AsyncClient

from backend.domain.entities.calorie import Calorie, Menu
from backend.domain.entities.meal import Meal
from backend.domain.repositories.calorie import CalorieRepository

PROMPT = """
너는 전문 영양사야. [{food}] 대괄호 안에 담긴 메뉴는 식판에 담긴 예상 음식 목록이야.

```json
{{
    "meals": [
        {{
            "name": "<name of the meal>",
            "calories": "<total calories of the meal if not available, use null>",
        }}
    ],
    "total_calories": "<total calories of all meals>",
}}
```

실제 사진에 담긴 식판을 보고, 음식의 종류와 양을 추론해서 상단의 JSON 형식으로 결과를 반환해줘.

최대한 칼로리와 음식의 종류를 정확하게 추론해줘.

만약 그럼에도 불구하고 음식의 종류나 칼로리를 정확하게 알 수 없다면, 해당 값을 null로 설정해줘.

내가 제공한 음식 목록과 예시를 참고해서 JSON만 작성해줘.
"""


class GeminiCalorieRepository(CalorieRepository):
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def get_calories(self, meal: Meal, image: IOBase) -> Calorie | None:
        menus = ", ".join(meal.dish_name.split("<br/>"))
        file = await self.client.files.upload(
            file=image,
            config={
                "mime_type": "image/jpeg",
            },
        )

        response = await self.client.models.generate_content(  # pyright: ignore[reportUnknownMemberType]
            model="gemini-2.0-flash",
            contents=[file, PROMPT.format(food=menus)],
        )

        if not response.text:
            return None

        json = response.text.replace("```json", "").replace("```", "")

        data = loads(json)
        meals = [
            Menu(name=menu["name"], calories=menu["calories"]) for menu in data["meals"]
        ]
        total_calories = data["total_calories"]

        return Calorie(meals=meals, total_calories=total_calories)
