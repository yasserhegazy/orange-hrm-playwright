import time

BASE_URL = "https://opensource-demo.orangehrmlive.com/"

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

LOGIN_PASSWORD = "Test12345@"


def generate_employee_data() -> dict:
    """Generate unique employee data for each test run."""
    suffix = str(int(time.time()))[-6:]
    return {
        "first_name": f"Test{suffix}",
        "middle_name": "Auto",
        "last_name": f"User{suffix}",
    }
