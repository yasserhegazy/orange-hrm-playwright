from playwright.sync_api import Page

from pages.pim.pim_page import PIMPage


class SideMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.pim_link = page.get_by_role("link", name="PIM")

    def navigate_to_pim(self) -> PIMPage:
        self.pim_link.click()

        return PIMPage(self.page)
