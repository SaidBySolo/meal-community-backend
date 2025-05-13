from sanic import json
from sanic.blueprints import Blueprint
from sanic_ext import validate

from backend.application.dtos.school import SearchSchoolDTO
from backend.application.use_cases.get.school import GetSchoolByName
from backend.infrastructure.sanic import BackendRequest

school = Blueprint("school_endpoint", url_prefix="/school")


@school.post("/search")
@validate(json=SearchSchoolDTO, body_argument="search_school_dto")
async def school_search(request: BackendRequest, search_school_dto: SearchSchoolDTO):
    results = await GetSchoolByName(request.app.ctx.neispy_school_repository).execute(
        search_school_dto.name
    )

    return json(
        {
            "results": [result.to_dict() for result in results],
        }
    )


@school.post("/info")
async def school_info(request: BackendRequest): ...
