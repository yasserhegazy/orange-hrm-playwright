import allure
import pytest
from playwright.sync_api import Page

from data.models import CreatedEmployee


def _extract_page_from_test_args(funcargs: dict) -> Page | None:
    page = funcargs.get("page") or funcargs.get("logged_in_page")
    if page is not None:
        return page

    created_employee = funcargs.get("created_employee")
    if isinstance(created_employee, CreatedEmployee):
        return created_employee.page

    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Attach screenshot and URL to Allure on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = _extract_page_from_test_args(item.funcargs)
        if page is None:
            return

        allure.attach(
            page.screenshot(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            page.url,
            name="failure-url",
            attachment_type=allure.attachment_type.TEXT,
        )
