from playwright.sync_api import Page, expect

from data.models import CandidateStatus
from pages.navigation.side_menu_page import SideMenuPage
from pages.recruitment.candidate_detail_page import STATUS_PREFIX
from tests.utils.generate_candidate_data import generate_candidate_data


class TestCandidateWorkflow:
    def test_add_candidate_and_reject(
        self,
        logged_in_page: Page,
        vacancy_for_recruitment: str,
        candidate_cleanup: list[str],
    ):
        candidate_data = generate_candidate_data(vacancy_name=vacancy_for_recruitment)
        candidate_full_name = f"{candidate_data.first_name} {candidate_data.last_name}"
        candidate_cleanup.append(candidate_full_name)

        # Navigate to Recruitment → Candidates → Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()

        # Add candidate and verify initial status
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        candidate_detail.wait_until_loaded()
        expect(candidate_detail.status_label).to_have_text(
            f"{STATUS_PREFIX}{CandidateStatus.APPLICATION_INITIATED.value}"
        )

        # Reject the candidate and verify final status
        candidate_detail.reject()
        expect(candidate_detail.status_label).to_have_text(f"{STATUS_PREFIX}{CandidateStatus.REJECTED.value}")

    def test_add_candidate_and_shortlist(
        self,
        logged_in_page: Page,
        vacancy_for_recruitment: str,
        candidate_cleanup: list[str],
    ):
        candidate_data = generate_candidate_data(vacancy_name=vacancy_for_recruitment)
        candidate_full_name = f"{candidate_data.first_name} {candidate_data.last_name}"
        candidate_cleanup.append(candidate_full_name)

        # Navigate to Recruitment → Candidates → Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()

        # Add candidate and verify initial status
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        candidate_detail.wait_until_loaded()
        expect(candidate_detail.status_label).to_have_text(
            f"{STATUS_PREFIX}{CandidateStatus.APPLICATION_INITIATED.value}"
        )

        # Shortlist the candidate and verify final status
        candidate_detail.shortlist()
        expect(candidate_detail.status_label).to_have_text(f"{STATUS_PREFIX}{CandidateStatus.SHORTLISTED.value}")
