from valkey.asyncio import Valkey

from backend.domain.entities.refresh_token import RefreshToken
from backend.domain.repositories.refresh_token import RefreshTokenRepository


class ValkeyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, valkey: Valkey, expires_in: int, prefix: str = "refresh_token"):
        self.valkey = valkey
        self.prefix = prefix
        super().__init__(expires_in)

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        await self.valkey.setex(
            f"{self.prefix}:{refresh_token.value}",
            self.expires_in,
            refresh_token.user_id,
        )
        return refresh_token

    async def get(self, refresh_token_value: str) -> RefreshToken | None:
        user_id = await self.valkey.get(f"{self.prefix}:{refresh_token_value}")
        if user_id:
            return RefreshToken(
                value=refresh_token_value,
                user_id=int(user_id),
            )

    async def delete(self, refresh_token_value: str) -> None:
        await self.valkey.delete(f"{self.prefix}:{ refresh_token_value}")

    async def update_ttl(self, refresh_token_value: str) -> None:
        await self.valkey.expire(
            f"{self.prefix}:{refresh_token_value}", self.expires_in
        )
