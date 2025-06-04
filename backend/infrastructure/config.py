from argparse import Namespace
from json import loads
from typing import Any, Callable, Optional, Sequence, Union, cast

from sanic.config import SANIC_PREFIX, Config

from backend import __version__


def list_converter(value: str) -> list[Any]:
    if value.startswith("["):
        return cast(list[Any], loads(value))
    raise ValueError


class BackendConfig(Config):
    def __init__(
        self,
        defaults: dict[str, Union[str, bool, int, float, None]] = {},
        env_prefix: Optional[str] = SANIC_PREFIX,
        keep_alive: Optional[bool] = None,
        *,
        converters: Optional[Sequence[Callable[[str], Any]]] = [list_converter],
    ):
        super().__init__(
            defaults=defaults,
            env_prefix=env_prefix,
            keep_alive=keep_alive,
            converters=converters,
        )
        # Default
        self.update(
            {
                # backend
                "CONFIG": "",
                "PRODUCTION": False,
                "USE_ENV": False,
                "SENTRY_DSN": "",
                "DB_URL": "sqlite+aiosqlite:///:memory:",
                "VALKEY_URL": "valkey://127.0.0.1:6379",
                "JWT_SECRET": "Psst, I see dead people",
                "ACCESS_TOKEN_EXP": 900,
                "REFRESH_TOKEN_EXP": 604800,
                "NEIS_API_KEY": "",
                "GEMINI_API_KEY": "",
                # Sanic config
                "HOST": "127.0.0.1",
                "PORT": 8000,
                "WORKERS": 1,
                "DEBUG": False,
                "ACCESS_LOG": False,
                "FORWARDED_SECRET": "",
                "FALLBACK_ERROR_FORMAT": "json",
                # Sanic ext config
                "OAS_UI_DEFAULT": "swagger",
                "OAS_URI_REDOC": False,
                # Open API config
                "SWAGGER_UI_CONFIGURATION": {
                    "apisSorter": "alpha",
                    "operationsSorter": "alpha",
                },
                "API_TITLE": "Backend",
                "API_VERSION": __version__,
                "API_LICENSE_NAME": "MIT",
            }
        )

    USE_ENV: bool
    CONFIG: str
    PRODUCTION: bool
    SENTRY_DSN: str
    DB_URL: str
    VALKEY_URL: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXP: int
    REFRESH_TOKEN_EXP: int
    NEIS_API_KEY: str
    GEMINI_API_KEY: str
    # Sanic config
    DEBUG: bool
    HOST: str
    PORT: int
    WORKERS: int

    def load_config_with_config_json(self, path: str) -> None:
        with open(path, "r") as f:
            config = loads(f.read())
            self.update_config(config)
        return None

    def update_with_args(self, args: Namespace) -> None:
        if not self.USE_ENV:
            self.update_config({k.upper(): v for k, v in vars(args).items()})
        if self.CONFIG:
            self.load_config_with_config_json(self.CONFIG)
        return None
