import pytest
from playwright.sync_api import Page

from data.constants import BASE_URL
from data.models import CreatedEmployee
from pages.navigation.side_menu_page import SideMenuPage
from pages.pim.employee_list_page import EmployeeListPage
from pages.pim.pim_page import PIMPage
from tests.support.flows import create_employee, login_as_admin

pytest_plugins = ["tests.plugins.allure_reporting"]


@pytest.fixture(autouse=True)
def goto(page: Page):
    """Fixture to navigate to the base URL."""
    page.goto(BASE_URL)


@pytest.fixture
def logged_in_page(page: Page, goto):
    """Fixture that logs in as admin and returns the page."""
    return login_as_admin(page)


@pytest.fixture
def created_employee(logged_in_page: Page) -> CreatedEmployee:
    """Create an employee and return its details for search tests."""
    return create_employee(logged_in_page)


@pytest.fixture
def employee_list_page(created_employee: CreatedEmployee) -> EmployeeListPage:
    """Navigate to PIM Employee List after an employee has been created."""
    page = created_employee.page
    SideMenuPage(page).navigate_to_pim()
    PIMPage(page)
    employee_list = EmployeeListPage(page)
    employee_list.wait_until_loaded()
    return employee_list
