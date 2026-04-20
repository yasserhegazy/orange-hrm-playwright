from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class CreatedEmployee:
    first_name: str
    last_name: str
    employee_id: str
    emp_number: str | None = None


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
    vacancy_id: str
    vacancy_name: str
    job_title: str
    status: VacancyStatus


class CandidateStatus(Enum):
    APPLICATION_INITIATED = "Application Initiated"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"


@dataclass(frozen=True)
class CandidateData:
    first_name: str
    last_name: str
    email: str
    vacancy_name: str
    candidate_id: str | None = None


@dataclass(frozen=True)
class CreatedCandidate:
    candidate_id: str
    first_name: str
    last_name: str
    email: str
    vacancy_name: str
