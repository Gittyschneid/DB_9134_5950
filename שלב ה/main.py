"""
Main application entry point.
Run this file to start the GUI:  python main.py
"""

import tkinter as tk
from tkinter import messagebox
from styles import (
    COLORS, FONTS, APP_TITLE, WINDOW_W, WINDOW_H,
    PAD_XS, PAD_S, PAD_M, PAD_L, PAD_XL,
)
from widgets import StyledButton, Card, StatCard, setup_treeview_style
from db import test_connection, run_query
from screens.staff_screen import StaffScreen
from screens.department_screen import DepartmentScreen
from screens.shift_screen import ShiftScreen
from screens.queries_screen import QueriesScreen
from screens.procedures_screen import ProceduresScreen


class App(tk.Tk):
    """Main application window. Manages navigation between screens using a sidebar."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(bg=COLORS["bg"])
        self.minsize(1100, 700)

        setup_treeview_style()

        # Layout: Sidebar (Left) + Main Content (Right)
        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_content = tk.Frame(self, bg=COLORS["bg"])
        self.main_content.pack(side="right", fill="both", expand=True)

        self.current_frame = None

        self._build_sidebar()
        self.show_home()

    def _build_sidebar(self):
        # App Title in Sidebar
        title_frame = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        title_frame.pack(fill="x", pady=(PAD_XL, PAD_M), padx=PAD_M)
        
        tk.Label(
            title_frame, text="MED",
            bg=COLORS["sidebar"], fg=COLORS["primary"],
            font=FONTS["title"], anchor="w",
        ).pack(side="left")
        
        tk.Label(
            title_frame, text="CORE",
            bg=COLORS["sidebar"], fg=COLORS["text_sidebar"],
            font=FONTS["title"], anchor="w",
        ).pack(side="left")

        tk.Frame(self.sidebar, bg=COLORS["text_secondary"], height=1).pack(fill="x", padx=PAD_M, pady=PAD_M)

        # Navigation Menu
        menu = [
            ("Dashboard",             lambda: self.show_home()),
            ("Staff Directory",       lambda: self.show_screen(StaffScreen)),
            ("Departments",           lambda: self.show_screen(DepartmentScreen)),
            ("Shifts & Scheduling",   lambda: self.show_screen(ShiftScreen)),
            ("Reports & Queries",     lambda: self.show_screen(QueriesScreen)),
            ("Procedures & Actions",  lambda: self.show_screen(ProceduresScreen)),
        ]

        for text, cmd in menu:
            btn = tk.Label(
                self.sidebar, text=text,
                bg=COLORS["sidebar"], fg=COLORS["text_muted"],
                font=FONTS["body_bold"], anchor="w",
                padx=PAD_M, pady=PAD_S, cursor="hand2"
            )
            btn.pack(fill="x", padx=PAD_S, pady=2)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, w=btn: w.config(bg="#1E293B", fg=COLORS["text_sidebar"]))
            btn.bind("<Leave>", lambda e, w=btn: w.config(bg=COLORS["sidebar"], fg=COLORS["text_muted"]))
            btn.bind("<Button-1>", lambda e, c=cmd: c())

        tk.Frame(self.sidebar, bg=COLORS["text_secondary"], height=1).pack(fill="x", padx=PAD_M, pady=PAD_M)

        # Exit Button
        exit_btn = tk.Label(
            self.sidebar, text="Exit System",
            bg=COLORS["sidebar"], fg=COLORS["danger"],
            font=FONTS["body_bold"], anchor="w",
            padx=PAD_M, pady=PAD_S, cursor="hand2"
        )
        exit_btn.pack(fill="x", padx=PAD_S, pady=2)
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#1E293B", fg="#F87171"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg=COLORS["sidebar"], fg=COLORS["danger"]))
        exit_btn.bind("<Button-1>", lambda e: self.destroy())

        # Connection Status at bottom
        self.status_bar = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        self.status_bar.pack(side="bottom", fill="x", pady=PAD_L, padx=PAD_M)

        ok, info = test_connection()
        status_text = "● Connected to DB" if ok else f"○ Offline\n{info[:30]}"
        status_fg = COLORS["success"] if ok else COLORS["danger"]

        self.status_label = tk.Label(
            self.status_bar, text=status_text,
            bg=COLORS["sidebar"], fg=status_fg,
            font=FONTS["small_bold"], anchor="w", justify="left"
        )
        self.status_label.pack(side="left")

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_home(self):
        self.clear()
        self.current_frame = HomeScreen(self.main_content, app=self)
        self.current_frame.pack(fill="both", expand=True)

    def show_screen(self, ScreenClass):
        self.clear()
        self.current_frame = ScreenClass(self.main_content, app=self)
        self.current_frame.pack(fill="both", expand=True)


class HomeScreen(tk.Frame):
    """Dashboard home screen."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        # Header Area
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=PAD_XL, pady=(PAD_XL, PAD_M))

        tk.Label(
            header, text="Overview",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["title"],
        ).pack(side="left")

        tk.Label(
            header, text="Clinical Operations Dashboard",
            bg=COLORS["bg"], fg=COLORS["text_muted"],
            font=FONTS["body"],
        ).pack(side="left", padx=PAD_M, pady=(8,0))

        # Stats Row
        stats_frame = tk.Frame(self, bg=COLORS["bg"])
        stats_frame.pack(fill="x", padx=PAD_XL, pady=(PAD_M, PAD_XL))

        staff_count = self._count("staff")
        dept_count = self._count("department")
        shift_count = self._count("staff_shift")

        for label, value, color in [
            ("Total Registered Staff", staff_count, COLORS["primary"]),
            ("Active Departments", dept_count, COLORS["accent"]),
            ("Recent Shift Assignments", shift_count, COLORS["success"]),
        ]:
            sc = StatCard(stats_frame, label, value, color_accent=color)
            sc.pack(side="left", expand=True, fill="x", padx=(0, PAD_M))

        # Welcome Card
        welcome_card = Card(self)
        welcome_card.pack(fill="both", expand=True, padx=PAD_XL, pady=(0, PAD_XL))

        tk.Label(
            welcome_card, text="Welcome to MedCore",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["heading"],
        ).pack(anchor="w", padx=PAD_L, pady=(PAD_L, PAD_S))

        tk.Label(
            welcome_card,
            text="Use the sidebar navigation to access different modules of the hospital management system.\n"
                 "The system provides interfaces for managing staff, scheduling shifts, and running operational reports.",
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=FONTS["body"], justify="left"
        ).pack(anchor="w", padx=PAD_L, pady=(0, PAD_M))

        # Footer
        tk.Label(
            self,
            text="System v2.0  •  Developed by Gitty Schneider & Avital Tal",
            bg=COLORS["bg"], fg=COLORS["text_muted"],
            font=FONTS["small"],
        ).pack(side="bottom", pady=PAD_M)

    def _count(self, table):
        try:
            res = run_query(f"SELECT COUNT(*) AS count FROM {table}")
            return str(res[0]["count"]) if res else "0"
        except Exception:
            return "—"


if __name__ == "__main__":
    app = App()
    app.mainloop()
