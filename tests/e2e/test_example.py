from playwright.sync_api import Page

from data.constants import VALID_PASSWORD, VALID_USERNAME
from pages.auth.login_page import LoginPage
from pages.navigation.dashboard_page import DashboardPage


def test_login_to_orangehrm(page: Page):
    login_page = LoginPage(page)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    DashboardPage(page)
