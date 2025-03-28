from asyncio import AbstractEventLoop
from functools import partial

from valkey.asyncio import Valkey


from backend.infrastructure.config import BackendConfig
from backend.adapters.controllers.endpoint import endpoint
from backend.infrastructure.jwt import jwt_decode, jwt_encode
from backend.infrastructure.sanic import Backend

from backend.infrastructure.sqlalchemy import SQLAlchemy
from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)
from backend.infrastructure.sqlalchemy.repositories.user import SQLAlchemyUserRepository


async def startup(app: Backend, loop: AbstractEventLoop) -> None:
    app.ctx.sa = await SQLAlchemy.create(app.config.DB_URL)
    app.ctx.valkey = Valkey.from_url(app.config.VALKEY_URL)
    app.ctx.user_repository = SQLAlchemyUserRepository(app.ctx.sa)
    app.ctx.refresh_token_repository = ValkeyRefreshTokenRepository(
        app.ctx.valkey, app.config.REFRESH_TOKEN_EXP
    )
    app.ctx.jwt_encode = partial(jwt_encode, secret=app.config.JWT_SECRET, exp=app.config.ACCESS_TOKEN_EXP)
    app.ctx.jwt_decode = partial(jwt_decode, secret=app.config.JWT_SECRET)


async def closeup(app: Backend, loop: AbstractEventLoop) -> None:
    await app.ctx.sa.engine.dispose()


def create_app(config: BackendConfig) -> Backend:
    backend = Backend("backend")
    backend.config.update(config)
    backend.blueprint(endpoint)
    backend.before_server_start(startup)
    backend.before_server_stop(closeup)

    return backend
