import pytest
from playwright.sync_api import Page

from data.constants import BASE_URL
from data.models import CreatedEmployee
from pages.navigation.side_menu_page import SideMenuPage
from pages.pim.employee_list_page import EmployeeListPage
from tests.plugins.employee import create_employee, login_as_admin

pytest_plugins = ["tests.plugins.allure_reporting"]


@pytest.fixture(autouse=True)
def goto(page: Page):
    """Fixture to navigate to the base URL."""
    page.goto(BASE_URL)


@pytest.fixture
def logged_in_page(page: Page):
    """Fixture that logs in as admin and returns the page."""
    return login_as_admin(page)


@pytest.fixture
def created_employee(logged_in_page: Page) -> CreatedEmployee:
    """Create an employee and return its details for search tests."""
    return create_employee(logged_in_page)


@pytest.fixture
def employee_list_page(logged_in_page: Page) -> EmployeeListPage:
    """Navigate to PIM Employee List and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()


@pytest.fixture
def employee_list_page_with_employee(created_employee: CreatedEmployee) -> EmployeeListPage:
    """Navigate to PIM Employee List after creating an employee."""
    return SideMenuPage(created_employee.page).navigate_to_pim().navigate_to_employee_list_page()
