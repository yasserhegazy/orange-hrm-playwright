from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from pages.navigation.side_menu_page import SideMenuPage


@pytest.fixture
def vacancy_cleanup(logged_in_page: Page) -> Generator[list[str]]:
    """Yield a list that tests append vacancy names to. Deletes all tracked vacancies after the test."""
    created_vacancy_names: list[str] = []

    yield created_vacancy_names

    if not created_vacancy_names:
        return

    try:
        vacancy_list_page = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_vacancies()
        for name in created_vacancy_names:
            try:
                vacancy_list_page.delete_vacancy_by_name(name)
            except Exception:
                pass
    except Exception:
        pass
