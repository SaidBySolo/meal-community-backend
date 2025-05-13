from types import SimpleNamespace
from typing import Any, Callable

from neispy import Neispy
from sanic.app import Sanic
from sanic.request import Request
from valkey.asyncio import Valkey

from backend.infrastructure.config import BackendConfig
from backend.infrastructure.neispy.repositories.meal import NeispyMealRepository
from backend.infrastructure.neispy.repositories.school import NeispySchoolRepository
from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.sqlalchemy.repositories.meal import SQLAlchemyMealRepository
from backend.infrastructure.sqlalchemy.repositories.user import SQLAlchemyUserRepository
from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)


class BackendContext(SimpleNamespace):
    sa: SQLAlchemy
    valkey: Valkey
    neispy: Neispy
    user_repository: SQLAlchemyUserRepository
    refresh_token_repository: ValkeyRefreshTokenRepository
    neispy_school_repository: NeispySchoolRepository
    neispy_meal_repository: NeispyMealRepository
    sa_meal_repository: SQLAlchemyMealRepository
    jwt_encode: Callable[[dict[str, Any]], str]
    jwt_decode: Callable[[str], dict[str, Any]]


class Backend(Sanic[BackendConfig, BackendContext]):
    ctx: BackendContext


class BackendRequest(Request):
    app: Backend
