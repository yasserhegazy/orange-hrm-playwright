import time

from playwright.sync_api import Page

from data.constants import (
    EMPLOYEE_FIRST_NAME,
    EMPLOYEE_LAST_NAME,
    EMPLOYEE_MIDDLE_NAME,
    LOGIN_PASSWORD,
)
from pages.add_employee_page import AddEmployeePage
from pages.dashboard_page import DashboardPage
from pages.employee_details_page import EmployeeDetailsPage
from pages.pim_page import PIMPage


def test_add_employee_without_login_details(logged_in_page: Page):
    dashboard = DashboardPage(logged_in_page)
    dashboard.is_displayed()
    dashboard.navigate_to_pim()

    pim = PIMPage(logged_in_page)
    pim.is_displayed()
    pim.click_add_employee()

    add_employee = AddEmployeePage(logged_in_page)
    add_employee.is_displayed()
    add_employee.fill_first_name(EMPLOYEE_FIRST_NAME)
    add_employee.fill_middle_name(EMPLOYEE_MIDDLE_NAME)
    add_employee.fill_last_name(EMPLOYEE_LAST_NAME)
    add_employee.click_save()

    employee_details = EmployeeDetailsPage(logged_in_page)
    employee_details.is_displayed()
    assert employee_details.get_first_name() == EMPLOYEE_FIRST_NAME
    assert employee_details.get_last_name() == EMPLOYEE_LAST_NAME


def test_add_employee_with_login_details(logged_in_page: Page):
    dashboard = DashboardPage(logged_in_page)
    dashboard.is_displayed()
    dashboard.navigate_to_pim()

    pim = PIMPage(logged_in_page)
    pim.is_displayed()
    pim.click_add_employee()

    add_employee = AddEmployeePage(logged_in_page)
    add_employee.is_displayed()
    add_employee.fill_first_name(EMPLOYEE_FIRST_NAME)
    add_employee.fill_middle_name(EMPLOYEE_MIDDLE_NAME)
    add_employee.fill_last_name(EMPLOYEE_LAST_NAME)

    add_employee.toggle_login_details()

    login_username = f"emp_{int(time.time())}"
    add_employee.fill_username(login_username)
    add_employee.fill_password(LOGIN_PASSWORD)
    add_employee.fill_confirm_password(LOGIN_PASSWORD)
    add_employee.click_save()

    employee_details = EmployeeDetailsPage(logged_in_page)
    employee_details.is_displayed()
    assert employee_details.get_first_name() == EMPLOYEE_FIRST_NAME
    assert employee_details.get_last_name() == EMPLOYEE_LAST_NAME
