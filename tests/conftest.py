from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, Page

from data.constants import LOGIN_PASSWORD
from data.models import CreatedCandidate, CreatedEmployee, CreatedVacancy, VacancyStatus
from pages.navigation.side_menu_page import SideMenuPage
from pages.pim.employee_list_page import EmployeeListPage
from pages.recruitment.candidate_list_page import CandidateListPage
from pages.recruitment.vacancy_list_page import VacancyListPage
from tests.plugins.candidate_api import create_candidate_using_api, delete_candidate_using_api
from tests.plugins.employee import add_employee_with_login_details, login_as_admin
from tests.plugins.employee_api import (
    create_employee_using_api,
    delete_employee_using_api,
    find_emp_number_by_employee_id,
)
from tests.plugins.vacancy_api import create_vacancy_using_api, delete_vacancy_using_api
from tests.utils.generate_candidate_data import generate_candidate_data
from tests.utils.generate_vacancy_data import generate_vacancy_data

pytest_plugins = [
    "tests.plugins.allure_reporting",
    "tests.plugins.vacancy_cleanup",
    "tests.plugins.candidate_cleanup",
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
def create_employee_api(logged_in_page: Page, request: pytest.FixtureRequest) -> Generator[CreatedEmployee]:
    """Create an employee via API and yield its details."""
    employee_data = getattr(request, "param", None)
    employee = create_employee_using_api(logged_in_page, employee_data=employee_data)
    yield employee
    try:
        delete_employee_using_api(logged_in_page, employee.emp_number or employee.employee_id)
    except AssertionError:
        pass


@pytest.fixture
def created_employee(create_employee_api: CreatedEmployee) -> CreatedEmployee:
    """Backward-compatible alias for API-created employee fixture."""
    return create_employee_api


@pytest.fixture
def create_hiring_manager(logged_in_page: Page) -> Generator[CreatedEmployee]:
    """Create an employee with login details to act as a Hiring Manager."""
    hm = add_employee_with_login_details(logged_in_page)
    yield hm
    try:
        delete_employee_using_api(logged_in_page, hm.emp_number or hm.employee_id)
    except AssertionError:
        pass


@pytest.fixture
def hiring_manager_page(browser: Browser, create_hiring_manager: CreatedEmployee, base_url: str) -> Generator[Page]:
    """Provide an isolated session logged in as the hiring manager."""
    context = browser.new_context()
    hm_page = context.new_page()
    hm_page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
    from pages.auth.login_page import LoginPage  # lazy import

    LoginPage(hm_page).login(create_hiring_manager.username, LOGIN_PASSWORD)
    yield hm_page
    context.close()


@pytest.fixture
def create_vacancy_api_for_hm(
    logged_in_page: Page,
    create_hiring_manager: CreatedEmployee,
) -> Generator[CreatedVacancy]:
    """Create a vacancy assigned to the hiring manager via API."""
    vacancy_data = generate_vacancy_data(
        job_title="QA Lead",
        hiring_manager=create_hiring_manager.first_name,
        status=VacancyStatus.ACTIVE,
    )

    hm_emp_number = create_hiring_manager.emp_number or find_emp_number_by_employee_id(
        logged_in_page, create_hiring_manager.employee_id
    )

    created_vacancy = create_vacancy_using_api(
        logged_in_page,
        vacancy_data=vacancy_data,
        hiring_manager_employee_id=hm_emp_number or create_hiring_manager.employee_id,
    )
    yield created_vacancy
    try:
        delete_vacancy_using_api(logged_in_page, created_vacancy.vacancy_id)
    except AssertionError:
        pass


@pytest.fixture
def hiring_manager(created_employee: CreatedEmployee) -> str:
    """Provide hiring manager name sourced from API-created employee."""
    return created_employee.first_name


@pytest.fixture
def employee_list_page(logged_in_page: Page) -> EmployeeListPage:
    """Navigate to PIM Employee List and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()


@pytest.fixture
def employee_list_page_with_employee(create_employee_api: CreatedEmployee, logged_in_page: Page) -> EmployeeListPage:
    """Navigate to PIM Employee List after creating an employee."""
    return SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()


@pytest.fixture
def vacancy_list_page(logged_in_page: Page) -> VacancyListPage:
    """Navigate to Recruitment Vacancies and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_vacancies()


@pytest.fixture
def create_vacancy_api(
    logged_in_page: Page,
    create_employee_api: CreatedEmployee,
    request: pytest.FixtureRequest,
) -> Generator[CreatedVacancy]:
    """Create a vacancy via API and yield its details."""
    vacancy_data = getattr(request, "param", None) or generate_vacancy_data(
        job_title="QA Lead",
        hiring_manager=create_employee_api.first_name,
        status=VacancyStatus.ACTIVE,
    )

    created_vacancy = create_vacancy_using_api(
        logged_in_page,
        vacancy_data=vacancy_data,
        hiring_manager_employee_id=create_employee_api.emp_number or create_employee_api.employee_id,
    )
    yield created_vacancy
    delete_vacancy_using_api(logged_in_page, created_vacancy.vacancy_id)


@pytest.fixture
def vacancy_for_recruitment(create_vacancy_api: CreatedVacancy) -> str:
    """Provide a pre-created vacancy name for recruitment tests."""
    return create_vacancy_api.vacancy_name


@pytest.fixture
def candidate_list_page(logged_in_page: Page) -> CandidateListPage:
    """Navigate to Recruitment Candidates and return its page object."""
    return SideMenuPage(logged_in_page).navigate_to_recruitment().navigate_to_candidates()


@pytest.fixture
def create_candidate_api(
    logged_in_page: Page,
    create_vacancy_api: CreatedVacancy,
    request: pytest.FixtureRequest,
) -> Generator[CreatedCandidate]:
    """Create a candidate via API and yield candidate data with candidate_id."""
    candidate_data = getattr(request, "param", None) or generate_candidate_data(
        vacancy_name=create_vacancy_api.vacancy_name,
    )

    created_candidate = create_candidate_using_api(
        logged_in_page,
        candidate_data=candidate_data,
        vacancy_id=create_vacancy_api.vacancy_id,
    )

    yield created_candidate

    delete_candidate_using_api(logged_in_page, created_candidate.candidate_id)
