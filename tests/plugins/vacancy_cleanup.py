from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from tests.plugins.recruitment_api import delete_vacancy_using_api, find_vacancy_id_by_name


@pytest.fixture
def vacancy_cleanup(logged_in_page: Page) -> Generator[list[str]]:
    """Yield a list that tests append vacancy names to. Deletes all tracked vacancies after the test."""
    created_vacancy_names: list[str] = []

    yield created_vacancy_names

    if not created_vacancy_names:
        return

    cleanup_errors: list[str] = []
    for vacancy_name in created_vacancy_names:
        try:
            vacancy_id = find_vacancy_id_by_name(logged_in_page, vacancy_name)
            if vacancy_id is None:
                cleanup_errors.append(f"{vacancy_name} (not found)")
                continue
            delete_vacancy_using_api(logged_in_page, vacancy_id)
        except AssertionError as exc:
            cleanup_errors.append(f"{vacancy_name} ({exc})")

    if cleanup_errors:
        raise AssertionError(
            "Failed to delete vacancies during cleanup:\n"
            + "\n".join(f"- {cleanup_error}" for cleanup_error in cleanup_errors)
        )
