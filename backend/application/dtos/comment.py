from dataclasses import asdict, dataclass
from datetime import datetime

from backend.application.dtos.user import PrivateUserDTO
from backend.domain.entities.comment import Comment
from backend.domain.utils import dict_factory


@dataclass
class CreateCommentDTO:
    meal_id: int
    """급식 ID"""
    content: str
    """댓글 내용"""
    parent_id: int | None = None
    """부모 댓글 ID"""


@dataclass
class GetCommentDTO:
    id: int
    """댓글 ID"""
    content: str
    """내용"""
    author: PrivateUserDTO
    """작성자"""
    replies: list["GetCommentDTO"]
    """대댓글"""
    created_at: datetime
    """생성일"""
    parent_id: int | None
    """부모 댓글 ID"""

    def to_dict(self):
        return asdict(self, dict_factory=dict_factory)

    @classmethod
    def from_entity(cls, entity: Comment) -> "GetCommentDTO":
        return cls(
            id=entity.id,
            content=entity.content,
            author=PrivateUserDTO.from_entity(entity.author),
            replies=[cls.from_entity(reply) for reply in entity.replies],
            created_at=entity.created_at,
            parent_id=entity.parent_id,
        )
