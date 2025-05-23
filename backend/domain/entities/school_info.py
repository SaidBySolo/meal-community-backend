from dataclasses import dataclass


@dataclass
class SchoolInfo:
    name: str
    """학교명"""
    edu_office_code: str
    """시도교육청코드"""
    standard_school_code: str
    """표준학교코드"""
