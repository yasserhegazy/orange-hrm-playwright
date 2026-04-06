import pytest

from data.models import VacancyStatus
from pages.navigation.side_menu_page import SideMenuPage
from pages.recruitment.vacancy_list_page import VacancyListPage
from tests.utils.generate_vacancy_data import generate_vacancy_data


class TestVacancyCreation:
    @pytest.mark.parametrize(
        ("job_title", "status"),
        [
            ("QA Lead", VacancyStatus.ACTIVE),
            ("Software Engineer", VacancyStatus.INACTIVE),
            ("Chief Executive Officer", VacancyStatus.ACTIVE),
        ],
        ids=[
            "active_qa_lead",
            "inactive_software_engineer",
            "active_ceo",
        ],
    )
    def test_create_vacancy(
        self,
        vacancy_list_page: VacancyListPage,
        vacancy_cleanup: list[str],
        hiring_manager: str,
        job_title: str,
        status: VacancyStatus,
    ):
        vacancy_data = generate_vacancy_data(job_title=job_title, hiring_manager=hiring_manager, status=status)
        vacancy_cleanup.append(vacancy_data.vacancy_name)

        vacancy_list = SideMenuPage(vacancy_list_page.page).navigate_to_recruitment().navigate_to_vacancies()
        add_vacancy_page = vacancy_list.click_add_vacancy()
        add_vacancy_page.create_vacancy(vacancy_data)

        vacancy_list = SideMenuPage(vacancy_list_page.page).navigate_to_recruitment().navigate_to_vacancies()
        assert vacancy_list.has_vacancy(vacancy_data.vacancy_name)
