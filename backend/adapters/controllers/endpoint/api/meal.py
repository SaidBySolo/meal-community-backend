from sanic import json
from sanic.blueprints import Blueprint
from sanic_ext import validate

from backend.application.dtos.meal import MealDTO
from backend.application.exceptions import MealNotFound
from backend.application.use_cases.create.meal import CreateMealUseCase
from backend.application.use_cases.get.meal import (
    GetDailyMealUseCase,
    GetDailyMealWithIDUseCase,
)
from backend.application.use_cases.get.user import GetUserByIDUseCase
from backend.infrastructure.jwt import require_auth
from backend.infrastructure.sanic import BackendRequest

meal = Blueprint("meal_endpoint", url_prefix="/meal")


@meal.post("/daily")
@validate(json=MealDTO, body_argument="meal_dto")
@require_auth
async def get_daily_meal(request: BackendRequest, user_id: str, meal_dto: MealDTO):
    user = await GetUserByIDUseCase(request.app.ctx.user_repository).execute(
        int(user_id)
    )

    edu_office_code = user.school_info.edu_office_code
    standard_school_code = user.school_info.standard_school_code

    try:
        results = await GetDailyMealWithIDUseCase(
            request.app.ctx.sa_meal_repository
        ).execute(
            edu_office_code,
            standard_school_code,
            meal_dto.date,
        )
    except MealNotFound:
        remote_results = await GetDailyMealUseCase(
            request.app.ctx.neispy_meal_repository
        ).execute(edu_office_code, standard_school_code, meal_dto.date)

        results = [
            (
                await CreateMealUseCase(request.app.ctx.sa_meal_repository).execute(
                    edu_office_code,
                    standard_school_code,
                    result,
                ),
                result,
            )
            for result in remote_results
        ]

    return json(
        {
            "results": [{"meal_id": id, **result.to_dict()} for id, result in results],
        }
    )
