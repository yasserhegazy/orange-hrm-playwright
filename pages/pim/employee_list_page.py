import re

from playwright.sync_api import Page, expect

NO_RECORDS_TEXT = "No Records Found"
RESULT_TEXT_HINT = "Record"
AUTOCOMPLETE_OPTION_SELECTOR = ".oxd-autocomplete-option"


class EmployeeListPage:
    def __init__(self, page: Page):
        self.page = page
        # OrangeHRM currently lacks dedicated test IDs, so I keep scoped text selectors as a fallback.
        self.employee_name_input = page.locator(".oxd-input-group", has_text="Employee Name").get_by_role("textbox")
        self.employee_id_input = page.locator(".oxd-input-group", has_text="Employee Id").get_by_role("textbox")
        self.search_button = page.get_by_role("button", name="Search")
        self.reset_button = page.get_by_role("button", name="Reset")
        self.no_records_text = page.locator("span.oxd-text.oxd-text--span", has_text=NO_RECORDS_TEXT)
        self.result_count_text = page.locator("span.oxd-text", has_text=RESULT_TEXT_HINT)

    def wait_until_loaded(self) -> None:
        expect(self.search_button).to_be_visible()
        expect(self.employee_name_input).to_be_visible()
        expect(self.employee_id_input).to_be_visible()

    def search_by_name(self, name: str) -> None:
        self.employee_name_input.fill(name)
        autocomplete_options = self.page.locator(AUTOCOMPLETE_OPTION_SELECTOR)
        expect(autocomplete_options.first).to_be_visible(timeout=5000)
        autocomplete_options.first.click()
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
        expect(self.result_count_text.or_(self.no_records_text)).to_be_visible()

    def click_reset(self) -> None:
        self.reset_button.click()

    def has_no_records(self) -> bool:
        return self.no_records_text.is_visible()

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
