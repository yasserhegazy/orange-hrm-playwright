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
        self.wait_until_loaded()

    def wait_until_loaded(self) -> VacancyListPage:
        """Wait for the vacancy list page to be fully loaded."""
        expect(self.header).to_be_visible()
        expect(self.result_rows.first.or_(self.no_records_text)).to_be_visible()
        return self

    @pw_trace()
    def click_add_vacancy(self) -> AddVacancyPage:
        self.add_button.click()

        return AddVacancyPage(self.page)

    def get_result_count(self) -> int:
        return self.result_rows.count()

    def has_vacancy(self, vacancy_name: str, timeout: int = 10000) -> bool:
        """Check if a vacancy with the given name exists in the list.

        Waits for the vacancy to appear before returning.
        """
        vacancy_row = self.result_rows.filter(has_text=vacancy_name)
        try:
            expect(vacancy_row.first).to_be_visible(timeout=timeout)
            return True
        except AssertionError:
            return False

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

        return True
