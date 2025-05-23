from dataclasses import asdict, dataclass, field
from datetime import datetime

from backend.domain.entities.school_info import SchoolInfo
from backend.domain.utils import dict_factory


@dataclass
class User:
    name: str
    """이름"""
    email: str
    """이메일"""
    password: str
    """비밀번호"""
    school_info: SchoolInfo
    """학교 정보"""
    grade: int
    """학년"""
    room: int
    """반"""
    created_at: datetime = field(init=False)
    """생성일"""

    def to_dict(self):
        return asdict(self, dict_factory=dict_factory)
