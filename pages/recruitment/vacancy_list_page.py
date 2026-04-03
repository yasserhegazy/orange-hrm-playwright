from playwright.sync_api import Page, expect

from pages.recruitment.add_vacancy_page import AddVacancyPage
from utils.tracing import pw_trace

NO_RECORDS_TEXT = "No Records Found"
RESULT_ROW_SELECTOR = "div.oxd-table-card"
DELETE_CONFIRMATION_BUTTON = "button.oxd-button--label-danger"


class VacancyListPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Vacancies")
        self.add_button = page.get_by_role("button", name="Add")
        self.result_rows = page.locator(RESULT_ROW_SELECTOR)
        self.no_records_text = page.locator("span.oxd-text.oxd-text--span", has_text=NO_RECORDS_TEXT)
        self.delete_confirmation_button = page.locator(DELETE_CONFIRMATION_BUTTON)
        expect(self.header).to_be_visible()

    @pw_trace()
    def click_add_vacancy(self) -> AddVacancyPage:
        self.add_button.click()

        return AddVacancyPage(self.page)

    def get_result_count(self) -> int:
        return self.result_rows.count()

    def has_vacancy(self, vacancy_name: str) -> bool:
        self.page.wait_for_timeout(1000)  # Wait for table to settle
        return self.result_rows.filter(has_text=vacancy_name).count() > 0

    @pw_trace("Delete Vacancy by Name")
    def delete_vacancy_by_name(self, vacancy_name: str) -> bool:
        row = self.result_rows.filter(has_text=vacancy_name)

        if row.count() == 0:
            return False

        delete_button = row.first.locator("button i.bi-trash")
        expect(delete_button).to_be_visible()
        delete_button.click()

        expect(self.delete_confirmation_button).to_be_visible()
        self.delete_confirmation_button.click()

        self.page.wait_for_load_state("networkidle", timeout=10000)
        return True
