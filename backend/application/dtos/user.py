from dataclasses import asdict, dataclass

from backend.domain.entities.school_info import SchoolInfo
from backend.domain.entities.user import User


@dataclass
class CreateUserDTO:
    name: str
    """이름"""
    email: str
    """이메일"""
    password: str
    """비밀번호"""
    grade: int
    """학년"""
    room: int
    """반"""
    school_info: SchoolInfo
    """학교 정보"""

    def to_dict(self):
        return asdict(self)

    def to_entity(self):
        return User(
            name=self.name,
            email=self.email,
            password=self.password,
            grade=self.grade,
            room=self.room,
            school_info=self.school_info,
        )


@dataclass
class LoginUserDTO:
    email: str
    """이메일"""
    password: str
    """비밀번호"""

    def to_dict(self):
        return asdict(self)


@dataclass
class JWTUserDTO:
    user_id: int
    """사용자 ID"""

    def to_dict(self):
        return asdict(self)
