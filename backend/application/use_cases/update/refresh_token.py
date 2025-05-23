from backend.domain.entities.refresh_token import RefreshToken
from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)


class UpdateRefreshTokenTTLUseCase:
    def __init__(self, refresh_token_repository: ValkeyRefreshTokenRepository):
        self.valkey_refresh_token_repository = refresh_token_repository

    async def execute(self, refresh_token: str) -> RefreshToken | None:
        return await self.valkey_refresh_token_repository.update_ttl(refresh_token)
