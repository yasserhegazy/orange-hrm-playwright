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

    def fill_first_name(self, name: str) -> None:
        self.first_name_input.fill(name)

    def fill_middle_name(self, name: str) -> None:
        self.middle_name_input.fill(name)

    def fill_last_name(self, name: str) -> None:
        self.last_name_input.fill(name)

    def add_employee(self, employee: dict[str, str]) -> None:
        self.fill_first_name(employee["first_name"])
        self.fill_middle_name(employee["middle_name"])
        self.fill_last_name(employee["last_name"])
        self.click_save()

    def toggle_login_details(self) -> None:
        self.login_details_toggle.click()

    def fill_username(self, username: str) -> None:
        username_input = self.page.locator(".oxd-input-group", has_text="Username").get_by_role("textbox")
        expect(username_input).to_be_visible()
        username_input.fill(username)

    def fill_password(self, password: str) -> None:
        self.password_input.first.fill(password)

    def fill_confirm_password(self, password: str) -> None:
        self.password_input.last.fill(password)

    def add_employee_with_login_details(self, employee: dict[str, str], username: str, password: str) -> None:
        self.fill_first_name(employee["first_name"])
        self.fill_middle_name(employee["middle_name"])
        self.fill_last_name(employee["last_name"])
        self.toggle_login_details()
        self.fill_username(username)
        self.fill_password(password)
        self.fill_confirm_password(password)
        self.click_save()

    def click_save(self) -> None:
        self.save_button.click()

    def get_employee_id(self) -> str:
        return self.page.locator(".oxd-input-group", has_text="Employee Id").get_by_role("textbox").input_value()
