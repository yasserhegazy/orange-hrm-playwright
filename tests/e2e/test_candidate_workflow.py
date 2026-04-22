from playwright.sync_api import Page

from data.models import CandidateData, CandidateStatus, CreatedVacancy
from pages.navigation.side_menu_page import SideMenuPage
from tests.utils.generate_candidate_data import generate_candidate_data


class TestCandidateWorkflow:
    def test_add_candidate_and_reject(
        self,
        logged_in_page: Page,
        create_vacancy_api_for_hm: CreatedVacancy,
        hiring_manager_page: Page,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api_for_hm.vacancy_name)
        candidate_cleanup.append(candidate_data)

        # Admin: Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        assert candidate_detail.get_status() == CandidateStatus.APPLICATION_INITIATED.value

        # HM: Reject Candidate
        hm_candidate_list = SideMenuPage(hiring_manager_page).navigate_to_recruitment().navigate_to_candidates()
        hm_candidate_detail = hm_candidate_list.open_candidate(candidate_data.first_name, candidate_data.last_name)
        hm_candidate_detail.reject()
        assert hm_candidate_detail.get_status() == CandidateStatus.REJECTED.value

    def test_add_candidate_and_shortlist(
        self,
        logged_in_page: Page,
        create_vacancy_api_for_hm: CreatedVacancy,
        hiring_manager_page: Page,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api_for_hm.vacancy_name)
        candidate_cleanup.append(candidate_data)

        # Admin: Add Candidate
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()
        candidate_detail = add_candidate_page.add_candidate(candidate_data)
        assert candidate_detail.get_status() == CandidateStatus.APPLICATION_INITIATED.value

        # HM: Shortlist Candidate
        hm_candidate_list = SideMenuPage(hiring_manager_page).navigate_to_recruitment().navigate_to_candidates()
        hm_candidate_detail = hm_candidate_list.open_candidate(candidate_data.first_name, candidate_data.last_name)
        hm_candidate_detail.shortlist()
        assert hm_candidate_detail.get_status() == CandidateStatus.SHORTLISTED.value


class TestAddCandidateWithFiles:
    def test_add_candidate_with_resume(
        self,
        logged_in_page: Page,
        create_vacancy_api: CreatedVacancy,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api.vacancy_name, with_resume=True)
        candidate_cleanup.append(candidate_data)

        # Add candidate with resume
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()
        candidate_detail = add_candidate_page.add_candidate(candidate_data)

        # Verify resume is attached
        assert candidate_detail.has_attachment("sample_cv.pdf")

    def test_add_candidate_with_resume_then_shortlist(
        self,
        logged_in_page: Page,
        create_vacancy_api: CreatedVacancy,
        candidate_cleanup: list[CandidateData],
    ):
        candidate_data = generate_candidate_data(vacancy_name=create_vacancy_api.vacancy_name, with_resume=True)
        candidate_cleanup.append(candidate_data)

        # Add candidate with resume
        candidate_list = SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()
        add_candidate_page = candidate_list.click_add_candidate()
        candidate_detail = add_candidate_page.add_candidate(candidate_data)

        # Shortlist
        candidate_detail.shortlist()

        # Verify resume is still attached after state transition
        assert candidate_detail.has_attachment("sample_cv.pdf")
