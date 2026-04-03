from playwright.sync_api import Page, expect

NO_RECORDS_TEXT = "No Records Found"
AUTOCOMPLETE_OPTION_SELECTOR = ".oxd-autocomplete-option"
LOADING_SPINNER_SELECTOR = ".oxd-loading-spinner-container"
RESULT_ROW_SELECTOR = "div.oxd-table-card"


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
        self.result_rows = self.page.locator(RESULT_ROW_SELECTOR)
        self.wait_until_loaded()

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

    def search_by_name_raw(self, name: str) -> None:
        self.employee_name_input.fill(name)
        self.click_search()

    def search_by_id(self, employee_id: str) -> None:
        self.employee_id_input.fill(employee_id)
        self.click_search()

    def click_search(self) -> None:
        self.search_button.click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
        expect(self.result_rows.or_(self.no_records_text).first).to_be_visible(timeout=5000)

    def click_reset(self) -> None:
        self.reset_button.click()

    def has_no_records(self) -> bool:
        return self.no_records_text.is_visible()

    def get_result_count(self) -> int:
        return self.result_rows.count()

    def has_result_row(self, expected_text: str) -> bool:
        return self.result_rows.filter(has_text=expected_text).count() > 0
