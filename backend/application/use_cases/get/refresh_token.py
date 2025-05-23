from backend.application.exceptions import BackendException
from backend.domain.entities.refresh_token import RefreshToken
from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)


class GetRefreshTokenUseCase:
    def __init__(self, refresh_token_repository: ValkeyRefreshTokenRepository):
        self.valkey_refresh_token_repository = refresh_token_repository

    async def execute(self, refresh_token_value: str) -> RefreshToken:
        nullable_refresh_token = await self.valkey_refresh_token_repository.get(
            refresh_token_value
        )

        if nullable_refresh_token:
            return nullable_refresh_token

        raise BackendException("Refresh token not found")
