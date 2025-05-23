from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from backend.domain.entities.user import User


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
