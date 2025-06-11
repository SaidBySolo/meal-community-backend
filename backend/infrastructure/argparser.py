from argparse import ArgumentParser, Namespace


def parse_args(argv: list[str]) -> Namespace:
    parser = ArgumentParser("heliotrope")

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The hostname to listen on (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The port of the webserver (default: 8000)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="The number of worker processes to spawn (default: 1)",
    )

    parser.add_argument(
        "--access-log",
        action="store_false",
        default=True,
        help="Disable the access log (default: False)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="The debug mode to use (default: False)",
    )

    config = parser.add_argument_group("config")

    config.add_argument(
        "--production",
        action="store_true",
        default=False,
        help="Run the server in production mode (default: False)",
    )

    config.add_argument(
        "--sentry-dsn",
        type=str,
        default="",
        help="The Sentry DSN to use (default: '')",
    )

    config.add_argument(
        "--db-url",
        type=str,
        default="sqlite+aiosqlite:///:memory:",
        help="The url of the sql database (default: '')",
    )

    config.add_argument(
        "--valkey-url",
        type=str,
        default="valkey://127.0.0.1:6379",
        help="The url of the valkey (default: 'valkey://127.0.0.1:6379')",
    )

    config.add_argument(
        "--jwt-secret",
        type=str,
        default="Psst, I see dead people",
        help="The secret to use for JWT (default: 'Psst, I see dead people')",
    )

    config.add_argument(
        "--access-token-exp",
        type=int,
        default=900,
        help="The expiration time for the access token (default: 3600)",
    )

    config.add_argument(
        "--refresh-token-exp",
        type=int,
        default=604800,
        help="The expiration time for the refresh token (default: 86400)",
    )

    config.add_argument(
        "--neis-api-key",
        type=str,
        default="",
        help="The API key for the NEIS API (default: '')",
    )

    config.add_argument(
        "--gemini-api-key",
        type=str,
        default="",
        help="The API key for the Gemini API (default: '')",
    )

    config.add_argument(
        "--forwarded-secret",
        type=str,
        default="",
        help="The secret to use for forwarded headers (default: '')",
    )
    config.add_argument(
        "--config",
        type=str,
        default="",
        help="The path to the config file (default: '')",
    )

    return parser.parse_args(argv)
