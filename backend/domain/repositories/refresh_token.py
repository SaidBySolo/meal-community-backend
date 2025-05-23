from abc import ABC, abstractmethod

from backend.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):
    @abstractmethod
    def __init__(self, expires_in: int):
        self.expires_in = expires_in

    @abstractmethod
    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def get(self, refresh_token_value: str) -> RefreshToken | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, refresh_token_value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_ttl(self, refresh_token_value: str) -> None:
        raise NotImplementedError
