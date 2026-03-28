from playwright.sync_api import Page

from pages.pim.employee_details_page import EmployeeDetailsPage
from tests.plugins.employee import add_employee_with_login_details, create_employee


def test_add_employee_without_login_details(page: Page, logged_in_page):
    employee = create_employee(logged_in_page)

    employee_details_page = EmployeeDetailsPage(page)
    assert employee_details_page.get_first_name() == employee.first_name
    assert employee_details_page.get_last_name() == employee.last_name


def test_add_employee_with_login_details(page: Page, logged_in_page):
    employee = add_employee_with_login_details(logged_in_page)

    employee_details_page = EmployeeDetailsPage(page)
    assert employee_details_page.get_first_name() == employee.first_name
    assert employee_details_page.get_last_name() == employee.last_name
