import re
from playwright.sync_api import Page, expect
     
def test_add_employee_to_orangehrm(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()
    expect(page).to_have_title(re.compile("OrangeHRM"))

    page.get_by_role("link", name="PIM").click()
    page.get_by_role("button", name="Add").click()

    page.get_by_placeholder("First Name").fill("Yasser")
    page.get_by_placeholder("Middle Name").fill("Osamah")
    page.get_by_placeholder("Last Name").fill("Hegazy")

    page.get_by_role("button", name="Save").click()
    # The next page after the redirect should have the text "Personal Details" visible
    expect(page.get_by_text("Personal Details")).to_be_visible(timeout=15000)
