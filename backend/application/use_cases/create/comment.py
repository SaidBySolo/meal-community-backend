from backend.application.exceptions import CommentNotFound, UserNotFound
from backend.domain.entities.comment import Comment
from backend.domain.enum import CreateCommentStatus
from backend.domain.repositories.comment import CommentRepository


class CreateNewCommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self, user_id: int, meal_id: int, comment: Comment) -> None:
        status = await self.comment_repository.create_new(user_id, meal_id, comment)
        if CreateCommentStatus.AUTHOR_NOT_FOUND == status:
            raise UserNotFound


class CreateReplyCommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self, user_id: int, meal_id: int, comment: Comment) -> None:
        status = await self.comment_repository.create_reply(user_id, meal_id, comment)
        if CreateCommentStatus.AUTHOR_NOT_FOUND == status:
            raise UserNotFound
        if CreateCommentStatus.PARENT_COMMENT_NOT_FOUND == status:
            raise CommentNotFound
        return


class CreateCommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(
        self,
        user_id: int,
        meal_id: int,
        comment: Comment,
    ) -> None:
        if comment.parent_id:
            return await CreateReplyCommentUseCase(self.comment_repository).execute(
                user_id, meal_id, comment
            )

        return await CreateNewCommentUseCase(self.comment_repository).execute(
            user_id, meal_id, comment
        )
