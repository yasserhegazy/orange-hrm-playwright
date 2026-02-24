import re
from playwright.sync_api import Page, expect


def test_add_employee_by_codegen(page: Page) -> None:
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("admin")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("link", name="Add Employee").click()
    page.get_by_role("textbox", name="First Name").click()
    page.get_by_role("textbox", name="First Name").fill("Yasser")
    page.get_by_role("textbox", name="Middle Name").click()
    page.get_by_role("textbox", name="Middle Name").fill("Osama")
    page.get_by_role("textbox", name="Last Name").click()
    page.get_by_role("textbox", name="Last Name").fill("Hegazy")
    page.get_by_role("textbox").nth(4).click()
    page.get_by_role("textbox").nth(4).fill("300")
    page.get_by_role("button", name="Save").click()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/169")
    page.get_by_role("heading", name="Personal Details").click()
    page.get_by_role("heading", name="Yasser Hegazy").click()
