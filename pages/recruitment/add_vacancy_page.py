import re

from playwright.sync_api import Page, expect

from data.models import VacancyData, VacancyStatus
from utils.tracing import pw_trace


class AddVacancyPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="Add Vacancy")
        self.vacancy_name_input = page.locator(".oxd-input-group", has_text="Vacancy Name").get_by_role("textbox")
        self.job_title_dropdown = page.locator(".oxd-input-group", has_text="Job Title").locator(".oxd-select-text")
        self.hiring_manager_input = page.locator(".oxd-input-group", has_text="Hiring Manager").get_by_role("textbox")
        self.num_positions_input = page.locator(".oxd-input-group", has_text="Number of Positions").get_by_role(
            "textbox"
        )
        self.status_toggle = page.locator(".oxd-switch-input").first
        self.save_button = page.get_by_role("button", name="Save")
        self.autocomplete_dropdown = page.locator(".oxd-autocomplete-dropdown")
        expect(self.header).to_be_visible()

    def fill_vacancy_name(self, name: str) -> None:
        self.vacancy_name_input.fill(name)

    def select_job_title(self, job_title: str) -> None:
        self.job_title_dropdown.click()
        option = self.page.locator(".oxd-select-dropdown").get_by_text(job_title, exact=True)
        expect(option).to_be_visible()
        option.click()

    def fill_hiring_manager(self, search_text: str) -> None:
        self.hiring_manager_input.fill(search_text)
        expect(self.autocomplete_dropdown).to_be_visible()

        valid_option = (
            self.autocomplete_dropdown.locator(".oxd-autocomplete-option")
            .filter(has_not_text="Searching")
            .filter(has_not_text="No Records Found")
            .filter(has_text=search_text)
            .first
        )

        expect(valid_option).to_be_visible(timeout=5000)
        valid_option.click()

    def fill_num_positions(self, num: int) -> None:
        self.num_positions_input.clear()
        self.num_positions_input.fill(str(num))

    def set_status(self, status: VacancyStatus) -> None:
        if status == VacancyStatus.INACTIVE:
            self.status_toggle.click()

    def click_save(self) -> None:
        self.save_button.click()
        expect(self.page).to_have_url(re.compile(r".*/addJobVacancy/\d+$"))

    @pw_trace("Create Vacancy")
    def create_vacancy(self, vacancy_data: VacancyData) -> None:
        self.fill_vacancy_name(vacancy_data.vacancy_name)
        self.select_job_title(vacancy_data.job_title)
        self.fill_hiring_manager(vacancy_data.hiring_manager)
        self.fill_num_positions(vacancy_data.num_positions)
        self.set_status(vacancy_data.status)
        self.click_save()
