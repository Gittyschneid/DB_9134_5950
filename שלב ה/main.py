"""
Main application entry point.
Run this file to start the GUI:  python main.py
"""

import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONTS, APP_TITLE, WINDOW_W, WINDOW_H, PAD_S, PAD_M, PAD_L, PAD_XL
from widgets import StyledButton, Card, StatCard, setup_treeview_style
from db import test_connection, run_query
from screens.staff_screen import StaffScreen
from screens.department_screen import DepartmentScreen
from screens.shift_screen import ShiftScreen
from screens.queries_screen import QueriesScreen
from screens.procedures_screen import ProceduresScreen


class App(tk.Tk):
    """Main application window. Manages navigation between screens."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(bg=COLORS["bg"])
        self.minsize(1000, 650)

        # Apply ttk styling
        setup_treeview_style()

        # Container holds all screens; one is shown at a time
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        # Show home screen first
        self.current_frame = None
        self.show_home()

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_home(self):
        self.clear()
        self.current_frame = HomeScreen(self.container, app=self)
        self.current_frame.pack(fill="both", expand=True)

    def show_screen(self, ScreenClass):
        self.clear()
        self.current_frame = ScreenClass(self.container, app=self)
        self.current_frame.pack(fill="both", expand=True)


class HomeScreen(tk.Frame):
    """Login/main menu - modern SaaS dashboard interface."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        # --- Top Banner with deep premium color ---
        banner = tk.Frame(self, bg=COLORS["primary"], height=130)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner, text="🏥  " + APP_TITLE,
            bg=COLORS["primary"], fg="white",
            font=FONTS["title"]
        ).pack(pady=(25, 4))
        
        tk.Label(
            banner, text="Stage 5 – Clinical Operations Dashboard",
            bg=COLORS["primary"], fg="#E0E7FF",  # soft indigo text
            font=FONTS["body_bold"]
        ).pack()

        # --- Connection Status Pill ---
        status_frame = tk.Frame(self, bg=COLORS["bg"])
        status_frame.pack(pady=(PAD_M, 0))
        
        ok, info = test_connection()
        status_text = "●  Database Connected (Live)" if ok else f"●  Database Offline: {info[:60]}"
        
        self.status_label = tk.Label(
            status_frame, text=status_text,
            bg=COLORS["bg"], fg=COLORS["success"] if ok else COLORS["danger"],
            font=FONTS["body_bold"]
        )
        self.status_label.pack()
        
        # Start the soft pulsing animation loop
        self.status_state = True
        self.pulse_connection(ok)

        # --- Live Metrics Statistics Row ---
        stats_frame = tk.Frame(self, bg=COLORS["bg"])
        stats_frame.pack(fill="x", padx=PAD_XL, pady=(PAD_L, 0))

        staff_count = self.get_count("staff")
        dept_count = self.get_count("department")
        shift_count = self.get_count("staff_shift")

        c1 = StatCard(stats_frame, "Total Registered Staff", staff_count, color_accent=COLORS["primary"])
        c1.pack(side="left", expand=True, fill="x", padx=PAD_S)

        c2 = StatCard(stats_frame, "Active Medical Departments", dept_count, color_accent=COLORS["accent"])
        c2.pack(side="left", expand=True, fill="x", padx=PAD_S)

        c3 = StatCard(stats_frame, "Total Assigned Shifts", shift_count, color_accent=COLORS["success"])
        c3.pack(side="left", expand=True, fill="x", padx=PAD_S)

        # --- Menu Navigation Card ---
        card = Card(self)
        card.pack(pady=PAD_L, padx=PAD_XL, fill="both", expand=True)

        tk.Label(
            card, text="Quick Management Console",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["heading"]
        ).pack(pady=(PAD_L, PAD_S), padx=PAD_XL)

        tk.Label(
            card, text="Select an operational component below to view records, run updates, or trigger procedures.",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"]
        ).pack(pady=(0, PAD_L))

        # --- Menu buttons grid (2x3 Layout) ---
        grid = tk.Frame(card, bg=COLORS["surface"])
        grid.pack(padx=PAD_XL, pady=(0, PAD_L), fill="both", expand=True)
        
        # Configure columns weight for uniform grid spacing
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        menu_items = [
            ("👨‍⚕️  Staff Directory",     "primary", lambda: app.show_screen(StaffScreen)),
            ("🏢  Departments",          "primary", lambda: app.show_screen(DepartmentScreen)),
            ("📅  Shifts & Scheduling",  "primary", lambda: app.show_screen(ShiftScreen)),
            ("🔍  Analytical Reports",   "accent",  lambda: app.show_screen(QueriesScreen)),
            ("⚙️  Procedures & Actions", "accent",  lambda: app.show_screen(ProceduresScreen)),
            ("🚪  Exit System",          "danger",  app.destroy),
        ]

        for i, (text, variant, cmd) in enumerate(menu_items):
            btn = StyledButton(grid, text=text, command=cmd, variant=variant)
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=PAD_M, pady=PAD_M, sticky="nsew")

        # --- Footer ---
        footer = tk.Label(
            self,
            text="Developed by: Gitty Schneider (333805950) & Avital Tal (214939134)  •  Academic Project",
            bg=COLORS["bg"], fg=COLORS["text_muted"],
            font=FONTS["small"]
        )
        footer.pack(side="bottom", pady=PAD_M)

    def get_count(self, table_name):
        """Helper to fetch rows count from the PostgreSQL database."""
        try:
            res = run_query(f"SELECT COUNT(*) AS count FROM {table_name}")
            return str(res[0]["count"]) if res else "0"
        except Exception:
            return "N/A"

    def pulse_connection(self, is_ok):
        """Soft pulsing animation for the connection indicator dot."""
        if not hasattr(self, "status_label") or not self.status_label.winfo_exists():
            return
        
        if is_ok:
            pulse_color = COLORS["success"] if self.status_state else "#86EFAC"  # Emerald vs Light Green
        else:
            pulse_color = COLORS["danger"] if self.status_state else "#FCA5A5"   # Red vs Light Red
            
        self.status_label.config(fg=pulse_color)
        self.status_state = not self.status_state
        self.after(1000, lambda: self.pulse_connection(is_ok))


if __name__ == "__main__":
    app = App()
    app.mainloop()
