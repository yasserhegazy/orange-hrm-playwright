from playwright.sync_api import Page

from pages.pim.pim_page import PIMPage
from pages.recruitment.recruitment_page import RecruitmentPage


class SideMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.sidebar = page.locator(".oxd-sidepanel")
        self.pim_link = self.sidebar.get_by_role("link", name="PIM")
        self.recruitment_link = self.sidebar.get_by_role("link", name="Recruitment")

    def navigate_to_pim(self) -> PIMPage:
        self.pim_link.click()
        self.page.wait_for_url("**/pim/**", timeout=10000)

        return PIMPage(self.page)

    def navigate_to_recruitment(self) -> RecruitmentPage:
        self.recruitment_link.click()
        self.page.wait_for_url("**/recruitment/**", timeout=10000)

        return RecruitmentPage(self.page)
