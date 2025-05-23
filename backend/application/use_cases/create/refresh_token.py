from secrets import token_urlsafe

from backend.domain.entities.refresh_token import RefreshToken
from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)


class CreateRefreshTokenUseCase:
    def __init__(self, refresh_token_repository: ValkeyRefreshTokenRepository):
        self.valkey_refresh_token_repository = refresh_token_repository

    async def execute(self, user_id: int) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            value=token_urlsafe(32),
        )
        return await self.valkey_refresh_token_repository.create(refresh_token)
