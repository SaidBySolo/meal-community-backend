from dataclasses import dataclass


@dataclass
class CreateCommentDTO:
    meal_id: int
    """급식 ID"""
    parent_id: int | None
    """부모 댓글 ID"""
    content: str
    """댓글 내용"""
