from playwright.sync_api import Page, expect

from pages.recruitment.add_candidate_page import AddCandidatePage
from pages.recruitment.candidate_detail_page import CandidateDetailPage
from utils.tracing import pw_trace

NO_RECORDS_TEXT = "No Records Found"
RESULT_ROW_SELECTOR = "div.oxd-table-card"


class CandidateListPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Candidates")
        self.add_button = page.get_by_role("button", name="Add")
        self.result_rows = page.locator(RESULT_ROW_SELECTOR)
        self.no_records_text = page.locator("span.oxd-text.oxd-text--span", has_text=NO_RECORDS_TEXT)
        self.delete_confirmation_button = page.get_by_role("button", name="Yes, Delete")
        self.wait_until_loaded()

    def wait_until_loaded(self) -> CandidateListPage:
        """Wait for the candidates list page to be fully loaded."""
        expect(self.header).to_be_visible()
        expect(self.result_rows.first.or_(self.no_records_text)).to_be_visible()
        return self

    @pw_trace()
    def click_add_candidate(self) -> AddCandidatePage:
        self.add_button.click()

        return AddCandidatePage(self.page)

    def get_result_count(self) -> int:
        return self.result_rows.count()

    @pw_trace("Open Candidate by Name")
    def open_candidate(self, first_name: str, last_name: str) -> CandidateDetailPage:
        """Find a candidate row by full name and open their detail page."""
        full_name = f"{first_name} {last_name}"
        row = self.result_rows.filter(has_text=full_name).first
        expect(row).to_be_visible(timeout=10000)
        row.get_by_role("link").click()
        return CandidateDetailPage(self.page)

    @pw_trace("Delete Candidate by Name")
    def delete_candidate_by_name(self, candidate_name: str, vacancy_name: str) -> bool:
        target_row = self.result_rows.filter(has_text=candidate_name).filter(has_text=vacancy_name)
        if target_row.count() == 0:
            return False

        delete_button = target_row.first.locator("button i.bi-trash")
        expect(delete_button).to_be_visible()
        delete_button.click()

        expect(self.delete_confirmation_button).to_be_visible()
        self.delete_confirmation_button.click()

        return True
