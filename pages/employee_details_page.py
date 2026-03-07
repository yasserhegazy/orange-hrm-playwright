from playwright.sync_api import Page, expect


class EmployeeDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Personal Details")

    def is_displayed(self):
        self.page.wait_for_url("**/viewPersonalDetails/**", timeout=60000)
        expect(self.header).to_be_visible(timeout=30000)

    def get_first_name(self) -> str:
        first_name = self.page.get_by_placeholder("First Name")
        expect(first_name).not_to_have_value("", timeout=10000)
        return first_name.input_value()

    def get_last_name(self) -> str:
        last_name = self.page.get_by_placeholder("Last Name")
        expect(last_name).not_to_have_value("", timeout=10000)
        return last_name.input_value()
