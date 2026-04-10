from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from pages.navigation.side_menu_page import SideMenuPage


@pytest.fixture
def candidate_cleanup(logged_in_page: Page) -> Generator[list[str]]:
    """Yield a list that tests append candidate names to. Deletes all tracked candidates after the test."""
    created_candidate_names: list[str] = []

    yield created_candidate_names

    if not created_candidate_names:
        return

    try:
        candidate_list_page = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        for name in created_candidate_names:
            try:
                candidate_list_page.delete_candidate_by_name(name)
            except Exception:
                pass
    except Exception:
        pass
