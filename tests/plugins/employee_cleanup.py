import pytest
from playwright.sync_api import Page

from pages.navigation.side_menu_page import SideMenuPage


class EmployeeCleanupTracker:
    def __init__(self):
        self._employee_ids: list[str] = []

    def register(self, employee_id: str) -> None:
        if employee_id and employee_id not in self._employee_ids:
            self._employee_ids.append(employee_id)

    @property
    def employee_ids(self) -> list[str]:
        return self._employee_ids.copy()

    def clear(self) -> None:
        self._employee_ids.clear()


@pytest.fixture
def employee_cleanup(logged_in_page: Page):
    tracker = EmployeeCleanupTracker()

    yield tracker

    if not tracker.employee_ids:
        return

        employee_list_page = SideMenuPage(logged_in_page).navigate_to_pim().navigate_to_employee_list_page()
        for employee_id in tracker.employee_ids:
            employee_list_page.delete_employee_by_id(employee_id)

    tracker.clear()
