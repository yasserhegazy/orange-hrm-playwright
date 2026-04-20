from playwright.sync_api import Page

from data.models import CandidateData, CandidateStatus, CreatedVacancy
from pages.navigation.side_menu_page import SideMenuPage
from tests.utils.generate_candidate_data import generate_candidate_data


class TestCandidateWorkflow:
    def test_add_candidate_and_reject(
        self,
        logged_in_page: Page,
        create_vacancy_api: CreatedVacancy,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api.vacancy_name)
        candidate_cleanup.append(candidate_data)

        # Navigate to Recruitment → Candidates → Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()

        # Add candidate and verify initial status
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        assert candidate_detail.get_status() == CandidateStatus.APPLICATION_INITIATED.value

        # Reject the candidate and verify final status
        candidate_detail.reject()
        assert candidate_detail.get_status() == CandidateStatus.REJECTED.value

    def test_add_candidate_and_shortlist(
        self,
        logged_in_page: Page,
        create_vacancy_api: CreatedVacancy,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api.vacancy_name)
        candidate_cleanup.append(candidate_data)

        # Navigate to Recruitment → Candidates → Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()

        # Add candidate and verify initial status
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        assert candidate_detail.get_status() == CandidateStatus.APPLICATION_INITIATED.value

        # Shortlist the candidate and verify final status
        candidate_detail.shortlist()
        assert candidate_detail.get_status() == CandidateStatus.SHORTLISTED.value
