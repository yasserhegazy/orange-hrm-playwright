from tests.utils.faker_instance import fake


def generate_employee_data() -> dict[str, str]:
    """Generate unique employee data for each test run."""
    return {
        "first_name": fake.unique.first_name(),
        "middle_name": fake.first_name(),
        "last_name": fake.last_name(),
        "employee_id": fake.unique.numerify(text="9#####"),
    }
