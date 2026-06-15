"""Department CRUD screen."""

from screens.crud_base import CRUDScreen


class DepartmentScreen(CRUDScreen):
    TABLE = "department"
    TITLE = "Department Management"
    PRIMARY_KEY = "department_id"
    FIELDS = [
        {"col": "department_name", "label": "Department Name", "type": "text"},
        {"col": "location",        "label": "Location",        "type": "text"},
    ]
    DISPLAY_QUERY = """
        SELECT department_id, department_name, location
        FROM department
        ORDER BY department_id
    """
