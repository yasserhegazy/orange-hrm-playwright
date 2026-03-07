from playwright.sync_api import Page, expect


class EmployeeDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Personal Details")

    def is_displayed(self):
        expect(self.header).to_be_visible()

    def get_first_name(self) -> str:
        return self.page.get_by_placeholder("First Name").input_value()

    def get_last_name(self) -> str:
        return self.page.get_by_placeholder("Last Name").input_value()
