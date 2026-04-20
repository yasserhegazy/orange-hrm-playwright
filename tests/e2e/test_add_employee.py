from playwright.sync_api import Page

from pages.pim.employee_details_page import EmployeeDetailsPage
from tests.plugins.employee import add_employee_with_login_details, create_employee
from tests.plugins.employee_api import delete_employee_using_api, find_emp_number_by_employee_id


def _cleanup_ui_employee(page: Page, employee_id: str) -> None:
    emp_number = find_emp_number_by_employee_id(page, employee_id)
    if emp_number:
        delete_employee_using_api(page, emp_number)


def test_add_employee_without_login_details(page: Page, logged_in_page, request):
    employee = create_employee(logged_in_page)
    request.addfinalizer(lambda: _cleanup_ui_employee(logged_in_page, employee.employee_id))

    employee_details_page = EmployeeDetailsPage(page)
    assert employee_details_page.get_first_name() == employee.first_name
    assert employee_details_page.get_last_name() == employee.last_name


def test_add_employee_with_login_details(page: Page, logged_in_page, request):
    employee = add_employee_with_login_details(logged_in_page)
    request.addfinalizer(lambda: _cleanup_ui_employee(logged_in_page, employee.employee_id))

    employee_details_page = EmployeeDetailsPage(page)
    assert employee_details_page.get_first_name() == employee.first_name
    assert employee_details_page.get_last_name() == employee.last_name
