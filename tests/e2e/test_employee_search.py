import pytest

from data.models import CreatedEmployee
from pages.pim.employee_list_page import EmployeeListPage


class TestEmployeeSearchByName:
    """Search PIM Employee List by employee name."""

    @pytest.mark.parametrize(
        "name_key",
        ["first_name", "last_name"],
        ids=["by_first_name", "by_last_name"],
    )
    def test_search_by_valid_name(
        self,
        created_employee: CreatedEmployee,
        employee_list_page_with_employee: EmployeeListPage,
        name_key: str,
    ):
        """Positive: searching by existing first/last name returns results."""
        expected_value = getattr(created_employee, name_key)
        employee_list_page_with_employee.search_by_name(expected_value)
        assert employee_list_page_with_employee.get_result_count() > 0
        assert employee_list_page_with_employee.has_result_row(expected_value)

    @pytest.mark.parametrize(
        "invalid_name",
        ["ZZZNOTEXIST999", "!@#$%NoUser"],
        ids=["gibberish_name", "special_chars_name"],
    )
    def test_search_by_invalid_name(
        self,
        employee_list_page: EmployeeListPage,
        invalid_name: str,
    ):
        """Negative: non-existent name shows No Records Found."""
        employee_list_page.search_by_name_raw(invalid_name)
        assert employee_list_page.has_no_records()


class TestEmployeeSearchById:
    """Search PIM Employee List by employee ID."""

    def test_search_by_valid_id(
        self,
        created_employee: CreatedEmployee,
        employee_list_page_with_employee: EmployeeListPage,
    ):
        """Positive: existing employee ID returns exactly 1 result."""
        employee_list_page_with_employee.search_by_id(created_employee.employee_id)
        assert employee_list_page_with_employee.get_result_count() == 1
        assert employee_list_page_with_employee.has_result_row(created_employee.employee_id)

    @pytest.mark.parametrize(
        "invalid_id",
        ["0000000", "9999999"],
        ids=["zero_id", "nonexistent_id"],
    )
    def test_search_by_invalid_id(
        self,
        employee_list_page: EmployeeListPage,
        invalid_id: str,
    ):
        """Negative: non-existent ID shows No Records Found."""
        employee_list_page.search_by_id(invalid_id)
        assert employee_list_page.has_no_records()
