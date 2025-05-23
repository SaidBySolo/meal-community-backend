from enum import Enum


class CreateCommentStatus(Enum):
    SUCCESS = "success"
    AUTHOR_NOT_FOUND = "author_not_found"
    PARENT_COMMENT_NOT_FOUND = "parent_comment_not_found"


class CreateMealStatus(Enum):
    SUCCESS = "success"
    SCHOOL_INFO_NOT_FOUND = "school_info_not_found"
