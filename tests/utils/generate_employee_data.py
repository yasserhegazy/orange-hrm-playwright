from tests.utils.faker_instance import fake


def generate_employee_data() -> dict[str, str]:
    """Generate unique employee data for each test run."""
    return {
        "first_name": f"{fake.first_name()}",
        "middle_name": fake.first_name(),
        "last_name": f"{fake.last_name()}",
    }
