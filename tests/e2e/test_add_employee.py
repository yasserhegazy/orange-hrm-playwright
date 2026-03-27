from playwright.sync_api import Page

from pages.pim.employee_details_page import EmployeeDetailsPage
from tests.support.flows import add_employee_with_login_details, create_employee


def test_add_employee_without_login_details(logged_in_page: Page):
    employee = create_employee(logged_in_page)

    employee_details = EmployeeDetailsPage(logged_in_page)
    assert employee_details.get_first_name() == employee.first_name
    assert employee_details.get_last_name() == employee.last_name


def test_add_employee_with_login_details(logged_in_page: Page):
    employee = add_employee_with_login_details(logged_in_page)

    employee_details = EmployeeDetailsPage(logged_in_page)
    assert employee_details.get_first_name() == employee.first_name
    assert employee_details.get_last_name() == employee.last_name
