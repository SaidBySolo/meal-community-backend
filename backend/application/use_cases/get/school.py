from backend.application.exceptions import SchoolNotFound
from backend.domain.entities.school import School
from backend.domain.repositories.school import SchoolRepository


class GetSchoolByName:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    async def execute(self, name: str) -> list[School]:
        result = await self.school_repository.get_by_name(name)
        if not result:
            raise SchoolNotFound("학교를 찾을 수 없습니다.")

        return result


class GetSchoolByCode:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    async def execute(self, edu_office_code: str, standard_school_code: str) -> School:
        result = await self.school_repository.get_by_code(
            edu_office_code, standard_school_code
        )
        if not result:
            raise SchoolNotFound("학교를 찾을 수 없습니다.")

        return result
