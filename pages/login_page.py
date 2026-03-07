from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.page.locator(".oxd-alert-content--error").text_content()

    def is_displayed(self):
        expect(self.login_button).to_be_visible()
