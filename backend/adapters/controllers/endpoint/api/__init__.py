from sanic.blueprints import Blueprint

from backend.adapters.controllers.endpoint.api.comment import comment
from backend.adapters.controllers.endpoint.api.meal import meal
from backend.adapters.controllers.endpoint.api.school import school
from backend.adapters.controllers.endpoint.api.user import user

api_endpoint = Blueprint.group(
    user,
    school,
    meal,
    comment,
    url_prefix="/api",
)
