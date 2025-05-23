from abc import ABC, abstractmethod
from typing import Optional

from backend.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_id_by_email_with_password(
        self, email: str, password: str
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_id_by_email(self, email: str) -> int | None:
        raise NotImplementedError
