import re

from playwright.sync_api import Page, expect

from pages.navigation.dashboard_page import DashboardPage


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def click_login(self) -> None:
        self.login_button.click()
        # Wait for navigation to dashboard to complete
        expect(self.page).to_have_url(re.compile(r".*/dashboard"), timeout=30000)

    def wait_until_loaded(self) -> None:
        expect(self.username_input).to_be_visible(timeout=15000)
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    def login(self, username: str, password: str) -> DashboardPage:
        self.wait_until_loaded()
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

        return DashboardPage(self.page)

    def get_error_message(self) -> str:
        return self.page.locator(".oxd-alert-content--error").text_content() or ""

    def is_displayed(self) -> None:
        expect(self.login_button).to_be_visible()
