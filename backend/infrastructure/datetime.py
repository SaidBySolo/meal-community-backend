from datetime import date, datetime


def to_datetime(date: str) -> datetime:
    """
    YYYYMMDD 형식의 문자열을 datetime으로 변환합니다.
    """
    return datetime.strptime(date.strip(), "%Y%m%d")


def to_date(date: str) -> date:
    """
    YYYYMMDD 형식의 문자열을 date로 변환합니다.
    """
    return datetime.strptime(date.strip(), "%Y%m%d").date()


def to_yyyymmdd(datetime: datetime | date) -> str:
    """
    datetime을 YYYYMMDD 형식의 문자열로 변환합니다.
    """
    return datetime.strftime("%Y%m%d")


def datetime_to_readable(date: datetime) -> str:
    """
    datetime을 YYYY년 MM월 DD일 형식의 문자열로 변환합니다.
    """
    return date.strftime("%Y{} %m{} %d{}").format("년", "월", "일")


def to_weekday(date: datetime) -> str:
    """
    datetime을 요일로 변환합니다.
    """
    days = ["월", "화", "수", "목", "금", "토", "일"]
    day = date.weekday()
    return days[day]
