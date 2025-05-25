from dataclasses import asdict, dataclass


@dataclass
class CreateCommentDTO:
    meal_id: int
    """급식 ID"""
    content: str
    """댓글 내용"""
    parent_id: int | None = None
    """부모 댓글 ID"""