from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from data.models import CandidateData
from tests.plugins.candidate_api import delete_candidate_using_api, find_candidate_id


@pytest.fixture
def candidate_cleanup(logged_in_page: Page) -> Generator[list[CandidateData]]:
    """Yield created candidates and delete them after the test."""
    created_candidates: list[CandidateData] = []

    yield created_candidates

    if not created_candidates:
        return

    cleanup_errors: list[str] = []
    for candidate in created_candidates:
        full_name = f"{candidate.first_name} {candidate.last_name}"
        try:
            candidate_id = candidate.candidate_id or find_candidate_id(logged_in_page, candidate)
            if candidate_id is None:
                cleanup_errors.append(f"{full_name} (vacancy: {candidate.vacancy_name}, not found)")
                continue
            delete_candidate_using_api(logged_in_page, candidate_id)
        except AssertionError as exc:
            cleanup_errors.append(f"{full_name} (vacancy: {candidate.vacancy_name}, {exc})")

    if cleanup_errors:
        raise AssertionError(
            "Failed to delete candidates during cleanup:\n"
            + "\n".join(f"- {cleanup_error}" for cleanup_error in cleanup_errors)
        )
