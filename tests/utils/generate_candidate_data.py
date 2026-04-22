from pathlib import Path

from data.models import CandidateData
from tests.utils.faker_instance import fake

# Anchor to the project root / data / uploads
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_UPLOADS_DIR = _PROJECT_ROOT / "data" / "uploads"


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
