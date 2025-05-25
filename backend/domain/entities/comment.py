from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List

from backend.domain.entities.user import User
from backend.domain.utils import dict_factory


@dataclass
class Comment:
    id: int = field(init=False)
    """댓글 ID"""
    content: str
    """내용"""
    author: User
    """작성자"""
    replies: List["Comment"] = field(default_factory=list["Comment"])
    """대댓글"""
    created_at: datetime = field(init=False)
    """생성일"""
    parent_id: int | None = field(default=None)
    """부모 댓글 ID"""

    def to_dict(self):
        return asdict(self, dict_factory=dict_factory)