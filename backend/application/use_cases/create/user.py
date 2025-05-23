from backend.application.dtos.user import CreateUserDTO
from backend.application.exceptions import UserAlreadyExists, UserNotFound
from backend.application.use_cases.get.user import GetUserIDByEmail
from backend.domain.entities.user import User
from backend.domain.repositories.user import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, create_user_dto: CreateUserDTO) -> User:
        try:
            await GetUserIDByEmail(self.user_repository).execute(create_user_dto.email)
        except UserNotFound:
            user = await self.user_repository.create(
                User(
                    email=create_user_dto.email,
                    password=create_user_dto.password,
                    name=create_user_dto.name,
                    grade=create_user_dto.grade,
                    room=create_user_dto.room,
                    school_info=create_user_dto.school_info,
                ),
            )
            return user

        raise UserAlreadyExists
