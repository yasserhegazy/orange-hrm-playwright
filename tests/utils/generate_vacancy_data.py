from data.models import VacancyData, VacancyStatus
from tests.utils.faker_instance import fake


def generate_vacancy_data(
    job_title: str,
    hiring_manager: str,
    status: VacancyStatus = VacancyStatus.ACTIVE,
    num_positions: int = 1,
) -> VacancyData:
    unique_suffix = fake.pystr(min_chars=6, max_chars=6)
    vacancy_name = f"{job_title} - {unique_suffix}"

    return VacancyData(
        job_title=job_title,
        vacancy_name=vacancy_name,
        hiring_manager=hiring_manager,
        status=status,
        num_positions=num_positions,
    )
