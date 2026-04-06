from playwright.sync_api import Page, expect

from pages.recruitment.vacancy_list_page import VacancyListPage
from utils.tracing import pw_trace


class RecruitmentPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Recruitment")
        self.vacancies_tab = page.get_by_role("link", name="Vacancies")
        self.candidates_tab = page.get_by_role("link", name="Candidates")
        expect(self.header).to_be_visible(timeout=10000)

    @pw_trace()
    def navigate_to_vacancies(self) -> VacancyListPage:
        self.vacancies_tab.click()

        return VacancyListPage(self.page)
