from abc import ABC, abstractmethod

from backend.domain.entities.school import School


class SchoolRepository(ABC):
    @abstractmethod
    async def get_school_by_name(self, name: str) -> list[School]:
        raise NotImplementedError

    @abstractmethod
    async def get_school_by_code(
        self, edu_office_code: str, standard_school_code: str
    ) -> School | None:
        raise NotImplementedError
