from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Dashboard")
        expect(self.heading).to_be_visible(timeout=15000)
