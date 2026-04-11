from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from data.models import CandidateData
from pages.navigation.side_menu_page import SideMenuPage


@pytest.fixture
def candidate_cleanup(logged_in_page: Page) -> Generator[list[CandidateData]]:
    """Yield created candidates and delete them after the test."""
    created_candidates: list[CandidateData] = []

    yield created_candidates

    if not created_candidates:
        return

    cleanup_errors: list[str] = []
    candidate_list_page = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
    for candidate in created_candidates:
        full_name = f"{candidate.first_name} {candidate.last_name}"
        deleted = candidate_list_page.delete_candidate_by_name(full_name, candidate.vacancy_name)
        if not deleted:
            cleanup_errors.append(f"{full_name} (vacancy: {candidate.vacancy_name})")

    if cleanup_errors:
        raise AssertionError(
            "Failed to delete candidates during cleanup:\n"
            + "\n".join(f"- {cleanup_error}" for cleanup_error in cleanup_errors)
        )
