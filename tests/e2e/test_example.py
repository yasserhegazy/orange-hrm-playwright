from playwright.sync_api import Page

from data.constants import VALID_PASSWORD, VALID_USERNAME
from pages.auth.login_page import LoginPage


def test_login_to_orangehrm(page: Page):
    login_page = LoginPage(page)
    dashboard_page = login_page.login(VALID_USERNAME, VALID_PASSWORD)
    assert dashboard_page is not None
