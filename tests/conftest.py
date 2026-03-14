import pytest
from playwright.sync_api import Page

from data.constants import BASE_URL, VALID_PASSWORD, VALID_USERNAME
from pages.login_page import LoginPage


@pytest.fixture(scope="function", autouse=True)
def goto(page: Page):
    """Fixture to navigate to the base URL."""
    page.goto(BASE_URL)


@pytest.fixture()
def login_with_admin(page: Page, goto):
    """Fixture that logs in as admin and returns the page."""
    login_page = LoginPage(page)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    return page
