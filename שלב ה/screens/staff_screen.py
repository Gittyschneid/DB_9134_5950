"""
Staff screen with tabs for Staff, Doctors, and Nurses.
"""

import tkinter as tk
from tkinter import ttk
from styles import COLORS, FONTS, PAD_L
from widgets import Header
from screens.crud_base import CRUDScreen


class StaffCRUD(CRUDScreen):
    TABLE = "staff"
    TITLE = "Staff"
    PRIMARY_KEY = "staff_id"
    FIELDS = [
        {"col": "first_name", "label": "First Name", "type": "text"},
        {"col": "last_name",  "label": "Last Name",  "type": "text"},
        {"col": "role",       "label": "Role",       "type": "text"},
        {"col": "phone",      "label": "Phone",      "type": "text"},
        {"col": "email",      "label": "Email",      "type": "text"},
        {"col": "hire_date",  "label": "Hire Date (YYYY-MM-DD)", "type": "text"},
        {"col": "department_id", "label": "Department",
         "type": "fk", "fk_table": "department",
         "fk_key": "department_id", "fk_display": "department_name"},
    ]
    # Note: no ID columns shown to user - we display names via JOIN
    DISPLAY_QUERY = """
        SELECT s.staff_id, s.first_name, s.last_name, s.role,
               s.phone, s.email, s.hire_date,
               d.department_name AS department
        FROM staff s
        LEFT JOIN department d ON s.department_id = d.department_id
        ORDER BY s.staff_id
        LIMIT 200
    """


class DoctorCRUD(CRUDScreen):
    TABLE = "doctor"
    TITLE = "Doctors"
    PRIMARY_KEY = "doctor_id"
    FIELDS = [
        {"col": "specialization",  "label": "Specialization",  "type": "text"},
        {"col": "license_number",  "label": "License Number",  "type": "text"},
        {"col": "staff_id",        "label": "Staff Member",
         "type": "fk", "fk_table": "staff",
         "fk_key": "staff_id", "fk_display": "first_name || ' ' || last_name"},
    ]
    DISPLAY_QUERY = """
        SELECT d.doctor_id, d.specialization, d.license_number,
               s.first_name || ' ' || s.last_name AS staff_name
        FROM doctor d
        LEFT JOIN staff s ON d.staff_id = s.staff_id
        ORDER BY d.doctor_id
        LIMIT 200
    """


class NurseCRUD(CRUDScreen):
    TABLE = "nurse"
    TITLE = "Nurses"
    PRIMARY_KEY = "nurse_id"
    FIELDS = [
        {"col": "certification", "label": "Certification", "type": "text"},
        {"col": "staff_id", "label": "Staff Member",
         "type": "fk", "fk_table": "staff",
         "fk_key": "staff_id", "fk_display": "first_name || ' ' || last_name"},
    ]
    DISPLAY_QUERY = """
        SELECT n.nurse_id, n.certification,
               s.first_name || ' ' || s.last_name AS staff_name
        FROM nurse n
        LEFT JOIN staff s ON n.staff_id = s.staff_id
        ORDER BY n.nurse_id
        LIMIT 200
    """


class StaffScreen(tk.Frame):
    """Container with three tabs: Staff, Doctors, Nurses."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        Header(self, title="Staff Management", on_back=app.show_home).pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        tab1 = StaffCRUD(notebook, app)
        tab2 = DoctorCRUD(notebook, app)
        tab3 = NurseCRUD(notebook, app)

        notebook.add(tab1, text="Staff")
        notebook.add(tab2, text="Doctors")
        notebook.add(tab3, text="Nurses")
