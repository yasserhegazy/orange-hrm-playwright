from pathlib import Path

from data.models import CandidateData
from tests.utils.faker_instance import fake

_UPLOADS_DIR = Path(__file__).parents[2] / "data" / "uploads"


def generate_candidate_data(
    vacancy_name: str,
    with_resume: bool = False,
) -> CandidateData:
    return CandidateData(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        vacancy_name=vacancy_name,
        resume=_UPLOADS_DIR / "sample_cv.pdf" if with_resume else None,
    )
