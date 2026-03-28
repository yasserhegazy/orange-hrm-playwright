from playwright.sync_api import Page, expect

from pages.pim.add_employee_page import AddEmployeePage
from pages.pim.employee_list_page import EmployeeListPage


class PIMPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_role("heading", name="PIM")
        self.add_button = page.get_by_role("button", name="Add")
        expect(self.header).to_be_visible()

    def click_add_employee(self) -> AddEmployeePage:
        self.add_button.click()

        return AddEmployeePage(self.page)

    def navigate_to_employee_list_page(self) -> EmployeeListPage:
        return EmployeeListPage(self.page)
