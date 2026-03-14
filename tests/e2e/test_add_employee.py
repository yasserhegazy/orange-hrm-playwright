import time

from playwright.sync_api import Page

from data.constants import LOGIN_PASSWORD, generate_employee_data
from pages.add_employee_page import AddEmployeePage
from pages.dashboard_page import DashboardPage
from pages.employee_details_page import EmployeeDetailsPage
from pages.pim_page import PIMPage
from pages.side_menu_page import SideMenuPage


def test_add_employee_without_login_details(login_with_admin: Page):
    DashboardPage(login_with_admin)

    side_menu = SideMenuPage(login_with_admin)
    side_menu.navigate_to_pim()

    pim = PIMPage(login_with_admin)
    pim.click_add_employee()

    employee = generate_employee_data()
    add_employee = AddEmployeePage(login_with_admin)
    add_employee.fill_first_name(employee["first_name"])
    add_employee.fill_middle_name(employee["middle_name"])
    add_employee.fill_last_name(employee["last_name"])
    add_employee.click_save()

    employee_details = EmployeeDetailsPage(login_with_admin)
    assert employee_details.get_first_name() == employee["first_name"]
    assert employee_details.get_last_name() == employee["last_name"]


def test_add_employee_with_login_details(login_with_admin: Page):
    DashboardPage(login_with_admin)

    side_menu = SideMenuPage(login_with_admin)
    side_menu.navigate_to_pim()

    pim = PIMPage(login_with_admin)
    pim.click_add_employee()

    employee = generate_employee_data()
    add_employee = AddEmployeePage(login_with_admin)
    add_employee.fill_first_name(employee["first_name"])
    add_employee.fill_middle_name(employee["middle_name"])
    add_employee.fill_last_name(employee["last_name"])

    add_employee.toggle_login_details()

    login_username = f"emp_{int(time.time())}"
    add_employee.fill_username(login_username)
    add_employee.fill_password(LOGIN_PASSWORD)
    add_employee.fill_confirm_password(LOGIN_PASSWORD)
    add_employee.click_save()

    employee_details = EmployeeDetailsPage(login_with_admin)
    assert employee_details.get_first_name() == employee["first_name"]
    assert employee_details.get_last_name() == employee["last_name"]
