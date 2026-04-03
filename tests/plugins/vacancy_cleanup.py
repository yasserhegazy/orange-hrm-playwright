import pytest
from playwright.sync_api import Page

from pages.navigation.side_menu_page import SideMenuPage


class VacancyCleanupTracker:
    def __init__(self):
        self._vacancy_names: list[str] = []

    def register(self, vacancy_name: str) -> None:
        if vacancy_name and vacancy_name not in self._vacancy_names:
            self._vacancy_names.append(vacancy_name)

    @property
    def vacancy_names(self) -> list[str]:
        return self._vacancy_names.copy()

    def clear(self) -> None:
        self._vacancy_names.clear()


@pytest.fixture
def vacancy_cleanup(logged_in_page: Page):
    tracker = VacancyCleanupTracker()

    yield tracker

    if not tracker.vacancy_names:
        return

    vacancy_list_page = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_vacancies()
    for vacancy_name in tracker.vacancy_names:
        vacancy_list_page.delete_vacancy_by_name(vacancy_name)

    tracker.clear()
