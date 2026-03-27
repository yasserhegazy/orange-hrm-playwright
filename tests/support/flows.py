import time

from playwright.sync_api import Page

from data.constants import LOGIN_PASSWORD, VALID_PASSWORD, VALID_USERNAME, generate_employee_data
from data.models import CreatedEmployee
from pages.auth.login_page import LoginPage
from pages.navigation.dashboard_page import DashboardPage
from pages.navigation.side_menu_page import SideMenuPage
from pages.pim.add_employee_page import AddEmployeePage
from pages.pim.employee_details_page import EmployeeDetailsPage
from pages.pim.pim_page import PIMPage


def login_as_admin(page: Page) -> Page:
    login_page = LoginPage(page)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    return page


def create_employee(page: Page) -> CreatedEmployee:
    DashboardPage(page)
    SideMenuPage(page).navigate_to_pim()
    PIMPage(page).click_add_employee()

    employee = generate_employee_data()
    add_employee_page = AddEmployeePage(page)
    employee_id = add_employee_page.get_employee_id()
    add_employee_page.add_employee(employee)
    EmployeeDetailsPage(page)

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
        page=page,
    )


def add_employee_with_login_details(page: Page) -> CreatedEmployee:
    DashboardPage(page)
    SideMenuPage(page).navigate_to_pim()
    PIMPage(page).click_add_employee()

    employee = generate_employee_data()
    add_employee_page = AddEmployeePage(page)
    employee_id = add_employee_page.get_employee_id()
    login_username = f"emp_{int(time.time())}"
    add_employee_page.add_employee_with_login_details(employee, username=login_username, password=LOGIN_PASSWORD)
    EmployeeDetailsPage(page)

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
        page=page,
    )
