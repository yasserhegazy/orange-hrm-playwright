from playwright.sync_api import Page


class SideMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.pim_link = page.get_by_role("link", name="PIM")

    def navigate_to_pim(self):
        self.pim_link.click()
