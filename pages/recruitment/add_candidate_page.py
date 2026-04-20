import re
from pathlib import Path

from playwright.sync_api import Page, expect

from data.models import CandidateData
from pages.recruitment.candidate_detail_page import CandidateDetailPage
from utils.tracing import pw_trace


class AddCandidatePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Add Candidate")
        self.first_name_input = page.get_by_placeholder("First Name")
        self.middle_name_input = page.get_by_placeholder("Middle Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.email_input = page.locator(".oxd-input-group", has_text="Email").get_by_role("textbox").first
        self.vacancy_dropdown = page.locator(".oxd-input-group", has_text="Vacancy").locator(".oxd-select-text")
        self.resume_input = page.locator("input[type='file']").first
        self.save_button = page.get_by_role("button", name="Save")
        expect(self.header).to_be_visible()

    def fill_first_name(self, name: str) -> None:
        self.first_name_input.fill(name)

    def fill_last_name(self, name: str) -> None:
        self.last_name_input.fill(name)

    def fill_email(self, email: str) -> None:
        self.email_input.fill(email)

    def select_vacancy(self, vacancy_name: str) -> None:
        self.vacancy_dropdown.click()
        option = self.page.locator(".oxd-select-dropdown").get_by_text(vacancy_name, exact=True)
        expect(option).to_be_visible()
        option.click()

    def upload_resume(self, file_path: Path) -> None:
        """Upload a résumé file via the hidden file input."""
        self.resume_input.set_input_files(str(file_path))

    def click_save(self) -> CandidateDetailPage:
        self.save_button.click()
        expect(self.page).to_have_url(re.compile(r".*/addCandidate/\d+$"), timeout=10000)
        return CandidateDetailPage(self.page)

    @pw_trace("Add Candidate")
    def add_candidate(self, candidate_data: CandidateData) -> CandidateDetailPage:
        self.fill_first_name(candidate_data.first_name)
        self.fill_last_name(candidate_data.last_name)
        self.fill_email(candidate_data.email)
        self.select_vacancy(candidate_data.vacancy_name)
        if candidate_data.resume is not None:
            self.upload_resume(candidate_data.resume)
        return self.click_save()
