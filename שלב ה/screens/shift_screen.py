"""Shift and Staff_Shift management screens."""

import tkinter as tk
from tkinter import ttk
from styles import COLORS, PAD_L
from widgets import Header
from screens.crud_base import CRUDScreen


class ShiftCRUD(CRUDScreen):
    TABLE = "shift"
    TITLE = "Shifts"
    PRIMARY_KEY = "shift_id"
    FIELDS = [
        {"col": "shift_name", "label": "Shift Name",     "type": "text"},
        {"col": "start_time", "label": "Start (HH:MM)",  "type": "text"},
        {"col": "end_time",   "label": "End (HH:MM)",    "type": "text"},
    ]
    DISPLAY_QUERY = """
        SELECT shift_id, shift_name, start_time, end_time
        FROM shift
        ORDER BY shift_id
    """


class StaffShiftCRUD(CRUDScreen):
    TABLE = "staff_shift"
    TITLE = "Staff Shift Assignments"
    PRIMARY_KEY = "staff_shift_id"
    FIELDS = [
        {"col": "shift_date", "label": "Shift Date (YYYY-MM-DD)", "type": "text"},
        {"col": "staff_id", "label": "Staff Member",
         "type": "fk", "fk_table": "staff",
         "fk_key": "staff_id", "fk_display": "first_name || ' ' || last_name"},
        {"col": "shift_id", "label": "Shift",
         "type": "fk", "fk_table": "shift",
         "fk_key": "shift_id", "fk_display": "shift_name"},
    ]
    # Show names not IDs - the assignment requirement
    DISPLAY_QUERY = """
        SELECT ss.staff_shift_id,
               ss.shift_date,
               s.first_name || ' ' || s.last_name AS staff_name,
               sh.shift_name
        FROM staff_shift ss
        LEFT JOIN staff s ON ss.staff_id = s.staff_id
        LEFT JOIN shift sh ON ss.shift_id = sh.shift_id
        ORDER BY ss.shift_date DESC
    """


class ShiftScreen(tk.Frame):
    """Container with tabs for Shifts and Assignments."""
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        Header(self, title="Shifts & Assignments", on_back=app.show_home).pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        notebook.add(ShiftCRUD(notebook, app),      text="Shifts")
        notebook.add(StaffShiftCRUD(notebook, app), text="Assignments")
