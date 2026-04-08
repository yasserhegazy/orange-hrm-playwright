from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from data.models import CreatedEmployee
from pages.navigation.side_menu_page import SideMenuPage
from pages.pim.employee_list_page import EmployeeListPage
from pages.recruitment.vacancy_list_page import VacancyListPage
from tests.plugins.employee import create_employee, login_as_admin

pytest_plugins = [
    "tests.plugins.allure_reporting",
    "tests.plugins.vacancy_cleanup",
]


@pytest.fixture(autouse=True)
def goto(page: Page, base_url: str):
    """Fixture to navigate to the base URL."""
    page.goto(base_url, wait_until="domcontentloaded", timeout=60000)


@pytest.fixture
def logged_in_page(page: Page):
    """Fixture that logs in as admin and returns the page."""
    return login_as_admin(page)


@pytest.fixture
def created_employee(logged_in_page: Page) -> Generator[CreatedEmployee]:
    """Create an employee, yield its details, and delete it after the test."""
    employee = create_employee(logged_in_page)
    yield employee
    try:
        employee_list_page = SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()
        employee_list_page.delete_employee_by_id(employee.employee_id)
    except Exception:
        pass


@pytest.fixture
def hiring_manager(logged_in_page: Page) -> Generator[str]:
    """Create an employee to serve as hiring manager, yield the name, and clean up after."""
    hiring_manager_employee = create_employee(logged_in_page)
    yield hiring_manager_employee.first_name
    try:
        employee_list_page = SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()
        employee_list_page.delete_employee_by_id(hiring_manager_employee.employee_id)
    except Exception:
        pass


@pytest.fixture
def employee_list_page(logged_in_page: Page) -> EmployeeListPage:
    """Navigate to PIM Employee List and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()


@pytest.fixture
def employee_list_page_with_employee(created_employee: CreatedEmployee) -> EmployeeListPage:
    """Navigate to PIM Employee List after creating an employee."""
    return SideMenuPage(created_employee.page).navigate_to_pim().navigate_to_employee_list_page()


@pytest.fixture
def vacancy_list_page(logged_in_page: Page) -> VacancyListPage:
    """Navigate to Recruitment Vacancies and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_vacancies()
