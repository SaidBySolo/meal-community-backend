from backend.application.exceptions import CommentNotFound
from backend.domain.entities.comment import Comment
from backend.domain.repositories.comment import CommentRepository


class GetCommentByMealIdUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self, meal_id: int) -> list[Comment]:
        comments = await self.comment_repository.get_by_meal_id(meal_id)
        if not comments:
            raise CommentNotFound
        return comments
