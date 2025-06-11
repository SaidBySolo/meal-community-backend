class BackendException(Exception):
    def __init__(self, *args: object, code: int = 400) -> None:
        self.code = code
        super().__init__(*args)


class UserAlreadyExists(BackendException):
    def __init__(self, message: str = "이미 존재하는 사용자입니다."):
        super().__init__(message)


class UserNotFound(BackendException):
    def __init__(self, message: str = "사용자를 찾을 수 없습니다."):
        super().__init__(message)


class IncorrectEmailOrPassword(BackendException):
    def __init__(self, message: str = "이메일 또는 비밀번호가 틀렸습니다."):
        super().__init__(message)


class PrefixNotBearer(BackendException):
    def __init__(self, message: str = "Prefix not Bearer."):
        super().__init__(message)


class NeedAuth(BackendException):
    def __init__(self, message: str = "로그인이 필요합니다."):
        super().__init__(message)


class SchoolNotFound(BackendException):
    def __init__(self, message: str = "학교를 찾을 수 없습니다."):
        super().__init__(message)


class MealNotFound(BackendException):
    def __init__(self, message: str = "급식을 찾을 수 없습니다."):
        super().__init__(message)


class CommentNotFound(BackendException):
    def __init__(self, message: str = "댓글을 찾을 수 없습니다."):
        super().__init__(message)


class CalorieNotFound(BackendException):
    def __init__(self, message: str = "칼로리 정보를 찾을 수 없습니다."):
        super().__init__(message)
