"""Employee API operations for OrangeHRM."""

from playwright.sync_api import Page

from data.models import CreatedEmployee, EmployeeData
from tests.plugins.api_helpers import _extract_data, _extract_id, _parse_json, _response_text
from tests.utils.generate_employee_data import generate_employee_data

EMPLOYEES_ENDPOINT = "/web/index.php/api/v2/pim/employees"


def create_employee_using_api(page: Page, employee_data: EmployeeData | None = None) -> CreatedEmployee:
    employee = employee_data or generate_employee_data()
    employee_id = employee.employee_id

    response = page.request.post(
        url=EMPLOYEES_ENDPOINT,
        data={
            "firstName": employee.first_name,
            "middleName": employee.middle_name,
            "lastName": employee.last_name,
            "empPicture": None,
            "employeeId": employee_id,
        },
    )

    payload = _parse_json(response, "create employee via API")
    data = _extract_data(payload)
    if not isinstance(data, dict):
        raise AssertionError("Unexpected employee create response shape")

    emp_number = _extract_id(data, ("empNumber", "id"), "employee")
    resolved_employee_id = (
        str(data.get("employeeId") or "").strip() or employee_id or _resolve_searchable_employee_id(page, emp_number)
    )

    return CreatedEmployee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        employee_id=resolved_employee_id,
        emp_number=emp_number,
    )


def delete_employee_using_api(page: Page, emp_number: str) -> None:
    response = page.request.delete(
        url=EMPLOYEES_ENDPOINT,
        data={"ids": [emp_number]},
        headers={"Content-Type": "application/json"},
    )
    assert response.ok, f"Failed to delete employee via API: {_response_text(response)}"


def _resolve_searchable_employee_id(page: Page, emp_number: str) -> str:
    response = page.request.get(url=f"{EMPLOYEES_ENDPOINT}/{emp_number}")
    payload = _parse_json(response, f"resolve employee details for empNumber '{emp_number}'")
    data = _extract_data(payload)

    if isinstance(data, dict):
        employee_id = str(data.get("employeeId") or "").strip()
        if employee_id:
            return employee_id

    # Fallback keeps fixture usable even if response shape changes.
    return emp_number


def find_emp_number_by_employee_id(page: Page, employee_id: str) -> str | None:
    """Look up an employee's internal empNumber using their display employeeId."""
    response = page.request.get(
        url=EMPLOYEES_ENDPOINT,
        params={"employeeId": employee_id},
    )
    payload = _parse_json(response, f"search employee by employeeId '{employee_id}'")
    data = _extract_data(payload)
    if isinstance(data, list) and data:
        return _extract_id(data[0], ("empNumber", "id"), "employee search result")
    return None
