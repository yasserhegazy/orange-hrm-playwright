from dataclasses import dataclass
from enum import Enum

from playwright.sync_api import Page


@dataclass(frozen=True)
class CreatedEmployee:
    first_name: str
    last_name: str
    employee_id: str
    page: Page


class VacancyStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Closed"


@dataclass(frozen=True)
class VacancyData:
    job_title: str
    vacancy_name: str
    hiring_manager: str
    status: VacancyStatus = VacancyStatus.ACTIVE
    num_positions: int = 1


@dataclass(frozen=True)
class CreatedVacancy:
    vacancy_name: str
    job_title: str
    status: VacancyStatus
    page: Page
