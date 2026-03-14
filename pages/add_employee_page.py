from playwright.sync_api import Page, expect


class AddEmployeePage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.middle_name_input = page.get_by_placeholder("Middle Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.login_details_toggle = page.locator(".oxd-switch-input")
        self.save_button = page.get_by_role("button", name="Save")
        self.password_input = page.locator("input[type='password']")
        expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()

    def fill_first_name(self, name: str):
        self.first_name_input.fill(name)

    def fill_middle_name(self, name: str):
        self.middle_name_input.fill(name)

    def fill_last_name(self, name: str):
        self.last_name_input.fill(name)

    def toggle_login_details(self):
        self.login_details_toggle.click()

    def fill_username(self, username: str):
        username_input = self.page.locator(
            ".oxd-input-group", has_text="Username"
        ).get_by_role("textbox")
        expect(username_input).to_be_visible()
        username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.first.fill(password)

    def fill_confirm_password(self, password: str):
        self.password_input.last.fill(password)

    def click_save(self):
        self.save_button.click()

    def get_employee_id(self) -> str:
        return self.page.locator(
            "div.oxd-form-row"
        ).filter(has_text="Employee Id").locator("input").input_value()
