from dataclasses import dataclass, field
from typing import List

from backend.domain.entities.user import User


@dataclass
class Comment:
    content: str
    """내용"""
    author: User
    """작성자"""
    created_at: str
    """생성일"""
    replies: List["Comment"] = field(default_factory=list["Comment"])
    """대댓글"""
    likes: int = 0
    """좋아요 수"""
