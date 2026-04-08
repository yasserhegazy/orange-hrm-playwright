from playwright.sync_api import Page

from data.constants import LOGIN_PASSWORD, VALID_PASSWORD, VALID_USERNAME
from data.models import CreatedEmployee
from pages.auth.login_page import LoginPage
from pages.navigation.side_menu_page import SideMenuPage
from tests.utils.faker_instance import fake
from tests.utils.generate_employee_data import generate_employee_data


def login_as_admin(page: Page) -> Page:
    login_page = LoginPage(page)
    dashboard_page = login_page.login(VALID_USERNAME, VALID_PASSWORD)
    assert dashboard_page is not None
    return page


def create_employee(page: Page) -> CreatedEmployee:
    add_employee_page = SideMenuPage(page).navigate_to_pim().click_add_employee()

    employee = generate_employee_data()
    employee_id = add_employee_page.get_employee_id()
    add_employee_page.add_employee(employee)

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
        page=page,
    )


def add_employee_with_login_details(page: Page) -> CreatedEmployee:
    add_employee_page = SideMenuPage(page).navigate_to_pim().click_add_employee()

    employee = generate_employee_data()
    employee_id = add_employee_page.get_employee_id()
    login_username = f"emp_{fake.pystr(min_chars=8, max_chars=8)}"
    add_employee_page.add_employee_with_login_details(employee, username=login_username, password=LOGIN_PASSWORD)

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
        page=page,
    )
