import time


def generate_employee_data() -> dict[str, str]:
    """Generate unique employee data for each test run."""
    unique_seed = str(time.time_ns())
    suffix = unique_seed[-6:]
    return {
        "first_name": f"Test{suffix}",
        "middle_name": "Auto",
        "last_name": f"User{suffix}",
    }
