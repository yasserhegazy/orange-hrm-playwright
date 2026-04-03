from dataclasses import dataclass

from playwright.sync_api import Page


@dataclass(frozen=True)
class CreatedEmployee:
    first_name: str
    last_name: str
    employee_id: str
    page: Page
