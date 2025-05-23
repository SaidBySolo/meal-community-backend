from backend.infrastructure.valkey.entities.repositories.refresh_token import (
    ValkeyRefreshTokenRepository,
)


class DeleteRefreshTokenUseCase:
    def __init__(self, refresh_token_repository: ValkeyRefreshTokenRepository):
        self.valkey_refresh_token_repository = refresh_token_repository

    async def execute(self, refresh_token: str) -> None:
        return await self.valkey_refresh_token_repository.delete(refresh_token)
