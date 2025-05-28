from abc import ABC, abstractmethod

from backend.domain.entities.comment import Comment
from backend.domain.enum import CreateCommentStatus


class CommentRepository(ABC):
    @abstractmethod
    async def create_new(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> CreateCommentStatus: ...

    @abstractmethod
    async def create_reply(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> CreateCommentStatus: ...

    @abstractmethod
    async def get_by_meal_id(self, meal_id: int) -> list[Comment]: ...

    @abstractmethod
    async def delete(self, comment_id: int) -> bool: ...

    @abstractmethod
    async def update_content(self, comment_id: int, content: str) -> Comment | None: ...
