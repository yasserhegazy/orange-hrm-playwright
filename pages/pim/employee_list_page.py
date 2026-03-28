import re

from playwright.sync_api import Page, expect

NO_RECORDS_TEXT = "No Records Found"
RESULT_TEXT_HINT = "Record"
AUTOCOMPLETE_OPTION_SELECTOR = ".oxd-autocomplete-option"
LOADING_SPINNER_SELECTOR = ".oxd-loading-spinner-container"


class EmployeeListPage:
    def __init__(self, page: Page):
        self.page = page
        self.employee_name_input = self.page.locator(".oxd-input-group", has_text="Employee Name").get_by_role(
            "textbox"
        )
        self.employee_id_input = self.page.locator(".oxd-input-group", has_text="Employee Id").get_by_role("textbox")
        self.search_button = self.page.get_by_role("button", name="Search")
        self.reset_button = self.page.get_by_role("button", name="Reset")
        self.no_records_text = self.page.locator("span.oxd-text.oxd-text--span", has_text=NO_RECORDS_TEXT)
        self.result_count_text = self.page.locator("span.oxd-text", has_text=RESULT_TEXT_HINT)

    def wait_until_loaded(self) -> None:
        expect(self.search_button).to_be_visible()
        expect(self.employee_name_input).to_be_visible()
        expect(self.employee_id_input).to_be_visible()

    def search_by_name(self, name: str) -> None:
        self.employee_name_input.fill(name)
        autocomplete_options = self.page.locator(AUTOCOMPLETE_OPTION_SELECTOR)
        expect(autocomplete_options.first).to_be_visible()
        autocomplete_options.first.click()
        self.click_search()

    def search_by_name_raw(self, name: str) -> None:
        self.employee_name_input.fill(name)
        self.click_search()

    def search_by_id(self, employee_id: str) -> None:
        self.employee_id_input.fill(employee_id)
        self.click_search()

    def search(self, name: str | None = None, employee_id: str | None = None) -> None:
        if name is not None:
            self.employee_name_input.fill(name)
        if employee_id is not None:
            self.employee_id_input.fill(employee_id)
        self.click_search()

    def click_search(self) -> None:
        self.search_button.click()
        loading_spinner = self.page.locator(LOADING_SPINNER_SELECTOR)
        if loading_spinner.is_visible(timeout=2000):
            expect(loading_spinner).not_to_be_visible(timeout=15000)
        final_state = self.result_count_text.or_(self.no_records_text)
        expect(final_state.first).to_be_visible(timeout=10000)

    def click_reset(self) -> None:
        self.reset_button.click()

    def has_no_records(self) -> bool:
        info_toast = self.page.locator(".oxd-toast-content-text", has_text=NO_RECORDS_TEXT)
        if info_toast.is_visible(timeout=2000):
            return True
        expect(self.result_count_text.or_(self.no_records_text).first).to_be_visible(timeout=10000)
        return self.no_records_text.is_visible() or info_toast.is_visible()

    def get_result_count(self) -> int:
        """Parse result count from badge text."""
        if self.has_no_records():
            return 0

        expect(self.result_count_text).to_be_visible()
        text = self.result_count_text.text_content() or ""
        match = re.search(r"\((\d+)\)", text)
        if not match:
            raise ValueError(f"Could not parse result count from text: {text!r}")
        return int(match.group(1))
