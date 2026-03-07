from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Dashboard")
        self.pim_link = page.get_by_role("link", name="PIM")

    def is_displayed(self):
        expect(self.heading).to_be_visible()

    def navigate_to_pim(self):
        self.pim_link.click()
