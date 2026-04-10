from data.models import CandidateData
from tests.utils.faker_instance import fake


def generate_candidate_data(vacancy_name: str) -> CandidateData:
    return CandidateData(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        vacancy_name=vacancy_name,
    )
