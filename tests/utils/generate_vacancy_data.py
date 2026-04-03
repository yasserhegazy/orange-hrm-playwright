import time

from data.models import VacancyData, VacancyStatus


def generate_vacancy_data(
    job_title: str,
    hiring_manager: str,
    status: VacancyStatus = VacancyStatus.ACTIVE,
    num_positions: int = 1,
) -> VacancyData:
    unique_seed = str(time.time_ns())
    suffix = unique_seed[-6:]
    vacancy_name = f"{job_title} - Test{suffix}"

    return VacancyData(
        job_title=job_title,
        vacancy_name=vacancy_name,
        hiring_manager=hiring_manager,
        status=status,
        num_positions=num_positions,
    )
