"""
Main application entry point.
Run this file to start the GUI:  python main.py
"""

import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONTS, APP_TITLE, WINDOW_W, WINDOW_H, PAD_M, PAD_L, PAD_XL
from widgets import StyledButton, Card, setup_treeview_style
from db import test_connection

# Import screens (you'll create these one by one)
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
        self.minsize(900, 600)

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
    """Login/main menu - the entry point to the system."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        # --- Top banner ---
        banner = tk.Frame(self, bg=COLORS["primary"], height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner, text="🏥  " + APP_TITLE,
            bg=COLORS["primary"], fg="white",
            font=FONTS["title"]
        ).pack(pady=(25, 5))
        tk.Label(
            banner, text="Stage 5 – Graphical Interface",
            bg=COLORS["primary"], fg="white",
            font=FONTS["body"]
        ).pack()

        # --- Connection status pill ---
        status_frame = tk.Frame(self, bg=COLORS["bg"])
        status_frame.pack(pady=(PAD_M, 0))
        ok, info = test_connection()
        status_color = COLORS["success"] if ok else COLORS["danger"]
        status_text = "● Database connected" if ok else f"● DB error: {info[:60]}"
        tk.Label(
            status_frame, text=status_text,
            bg=COLORS["bg"], fg=status_color,
            font=FONTS["small"]
        ).pack()

        # --- Menu card ---
        card = Card(self)
        card.pack(pady=PAD_XL, padx=PAD_XL)

        tk.Label(
            card, text="Main Menu",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["heading"]
        ).pack(pady=(PAD_L, PAD_M), padx=PAD_XL * 2)

        tk.Label(
            card, text="Select a section to manage",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"]
        ).pack(pady=(0, PAD_L))

        # --- Menu buttons grid ---
        grid = tk.Frame(card, bg=COLORS["surface"])
        grid.pack(padx=PAD_XL, pady=(0, PAD_XL))

        menu_items = [
            ("👨‍⚕️  Staff Management",   "primary", lambda: app.show_screen(StaffScreen)),
            ("🏢  Departments",          "primary", lambda: app.show_screen(DepartmentScreen)),
            ("📅  Shifts & Assignments", "primary", lambda: app.show_screen(ShiftScreen)),
            ("🔍  Reports & Queries",    "accent",  lambda: app.show_screen(QueriesScreen)),
            ("⚙️  Procedures & Functions","accent", lambda: app.show_screen(ProceduresScreen)),
            ("🚪  Exit",                 "danger",  app.destroy),
        ]

        for i, (text, variant, cmd) in enumerate(menu_items):
            btn = StyledButton(grid, text=text, command=cmd, variant=variant, width=28)
            btn.grid(row=i // 2, column=i % 2, padx=PAD_M, pady=PAD_M, sticky="ew")

        # --- Footer ---
        footer = tk.Label(
            self,
            text="Gitty Schneider (333805950)  •  Avital Tal (214939134)",
            bg=COLORS["bg"], fg=COLORS["text_muted"],
            font=FONTS["small"]
        )
        footer.pack(side="bottom", pady=PAD_M)


if __name__ == "__main__":
    app = App()
    app.mainloop()
