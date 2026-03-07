from playwright.sync_api import Page, expect


class PIMPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="PIM")
        self.add_button = page.get_by_role("button", name="Add")

    def is_displayed(self):
        expect(self.header).to_be_visible()

    def click_add_employee(self):
        self.add_button.click()
