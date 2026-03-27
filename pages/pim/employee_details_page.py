from playwright.sync_api import Page, expect


class EmployeeDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Personal Details")
        expect(self.header).to_be_visible(timeout=30000)

    def get_first_name(self) -> str:
        first_name = self.page.get_by_placeholder("First Name")
        expect(first_name).not_to_have_value("")
        return first_name.input_value()

    def get_last_name(self) -> str:
        last_name = self.page.get_by_placeholder("Last Name")
        expect(last_name).not_to_have_value("")
        return last_name.input_value()
