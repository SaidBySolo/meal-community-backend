from neispy import Neispy
from neispy.error import DataNotFound

from backend.domain.entities.school import School
from backend.domain.repositories.school import SchoolRepository
from backend.infrastructure.neispy.entities.school import NeispySchool


class NeispySchoolRepository(SchoolRepository):
    def __init__(self, neispy: Neispy):
        self.neispy = neispy

    async def get_by_name(self, name: str) -> list[School]:
        try:
            result = await self.neispy.schoolInfo(SCHUL_NM=name)
        except DataNotFound:
            return []
        return [NeispySchool.from_neispy(school) for school in result.schoolInfo[1].row]

    async def get_by_code(
        self, edu_office_code: str, standard_school_code: str
    ) -> School | None:
        try:
            result = await self.neispy.schoolInfo(
                ATPT_OFCDC_SC_CODE=edu_office_code,
                SD_SCHUL_CODE=standard_school_code,
            )
        except DataNotFound:
            return None
        return NeispySchool.from_neispy(result.schoolInfo[1].row[0])
