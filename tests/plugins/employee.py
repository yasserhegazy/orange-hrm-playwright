from playwright.sync_api import Page

from data.constants import LOGIN_PASSWORD, VALID_PASSWORD, VALID_USERNAME
from data.models import CreatedEmployee
from pages.auth.login_page import LoginPage
from pages.navigation.side_menu_page import SideMenuPage
from tests.plugins.recruitment_api import create_employee_using_api as create_employee_via_api
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
    employee_id = fake.unique.numerify(text="9#####")
    add_employee_page.add_employee(employee, employee_id=employee_id)

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
    )


def add_employee_with_login_details(page: Page) -> CreatedEmployee:
    add_employee_page = SideMenuPage(page).navigate_to_pim().click_add_employee()

    employee = generate_employee_data()
    employee_id = fake.unique.numerify(text="9#####")
    login_username = fake.unique.bothify(text="emp_########")
    add_employee_page.add_employee_with_login_details(
        employee,
        employee_id=employee_id,
        username=login_username,
        password=LOGIN_PASSWORD,
    )

    return CreatedEmployee(
        first_name=employee["first_name"],
        last_name=employee["last_name"],
        employee_id=employee_id,
    )


def create_employee_using_api(page: Page, employee_data: dict[str, str] | None = None) -> CreatedEmployee:
    """Create an employee via API and return its key details."""
    return create_employee_via_api(page, employee_data)
