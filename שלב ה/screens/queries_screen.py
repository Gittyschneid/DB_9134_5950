"""
Queries screen.
Runs SELECT queries from Stage 2 with nice presentation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS, PAD_S, PAD_M, PAD_L
from widgets import StyledButton, Card, Header
from db import run_query


class QueriesScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        Header(self, title="Reports & Queries", on_back=app.show_home).pack(fill="x")

        # --- Controls panel ---
        controls = Card(self)
        controls.pack(fill="x", padx=PAD_L, pady=PAD_L, ipadx=PAD_L, ipady=PAD_M)

        tk.Label(
            controls, text="Available Reports",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"]
        ).pack(anchor="w", padx=PAD_M, pady=(PAD_S, PAD_M))

        btn_row = tk.Frame(controls, bg=COLORS["surface"])
        btn_row.pack(anchor="w", padx=PAD_M, pady=(0, PAD_S))

        StyledButton(
            btn_row,
            text="📊  Monthly Workload Report",
            command=self.run_monthly_workload,
            variant="primary", width=30
        ).grid(row=0, column=0, padx=PAD_S, pady=PAD_S)

        StyledButton(
            btn_row,
            text="🏥  Understaffed Departments",
            command=self.run_understaffed_depts,
            variant="primary", width=30
        ).grid(row=0, column=1, padx=PAD_S, pady=PAD_S)

        # --- Description area ---
        self.desc_label = tk.Label(
            self, text="Click a report above to run it.",
            bg=COLORS["bg"], fg=COLORS["text_muted"],
            font=FONTS["body"], anchor="w", justify="left"
        )
        self.desc_label.pack(fill="x", padx=PAD_L, pady=(0, PAD_S))

        # --- Results table ---
        result_frame = tk.Frame(self, bg=COLORS["surface"])
        result_frame.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))

        self.tree = ttk.Treeview(result_frame, show="headings")
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    # -------------------------- Queries ---------------------------------
    def run_monthly_workload(self):
        """SELECT 1 from Stage 2: shifts per staff per month."""
        self.desc_label.config(
            text="📊  Monthly Workload Report — shifts per staff member per month."
        )
        query = """
            SELECT
                s.first_name || ' ' || s.last_name AS staff_name,
                s.role,
                TO_CHAR(ss.shift_date, 'YYYY-MM') AS month,
                COUNT(*) AS shifts_count
            FROM staff_shift ss
            JOIN staff s ON ss.staff_id = s.staff_id
            GROUP BY s.first_name, s.last_name, s.role, TO_CHAR(ss.shift_date, 'YYYY-MM')
            ORDER BY month DESC, shifts_count DESC
            LIMIT 100
        """
        self._show_query_results(query)

    def run_understaffed_depts(self):
        """SELECT 2 from Stage 2: departments with fewer than 30 nurses."""
        self.desc_label.config(
            text="🏥  Departments with fewer than 30 nurses — staffing analysis."
        )
        query = """
            SELECT
                d.department_name,
                d.location,
                COUNT(n.nurse_id) AS nurse_count
            FROM department d
            LEFT JOIN staff s ON s.department_id = d.department_id
            LEFT JOIN nurse n ON n.staff_id = s.staff_id
            GROUP BY d.department_id, d.department_name, d.location
            HAVING COUNT(n.nurse_id) < 30
            ORDER BY nurse_count ASC
        """
        self._show_query_results(query)

    # -------------------------- Helpers ---------------------------------
    def _show_query_results(self, query):
        try:
            rows = run_query(query)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))
            return

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not rows:
            self.tree["columns"] = ("info",)
            self.tree.heading("info", text="No results")
            return

        cols = list(rows[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=160, anchor="w")

        for r in rows:
            self.tree.insert("", "end", values=[r[c] for c in cols])
