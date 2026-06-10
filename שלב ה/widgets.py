"""
Reusable styled widgets.
Use these instead of raw tk.Button etc. to keep the UI consistent.
"""

import tkinter as tk
from tkinter import ttk
from styles import COLORS, FONTS, PAD_S, PAD_M


class StyledButton(tk.Button):
    """A nicer-looking button with hover effect."""
    def __init__(self, parent, text, command=None, variant="primary", width=18, **kwargs):
        colors_map = {
            "primary": (COLORS["primary"], COLORS["primary_hover"], "white"),
            "success": (COLORS["success"], "#1e8449", "white"),
            "danger":  (COLORS["danger"], "#922b21", "white"),
            "warning": (COLORS["warning"], "#b9651b", "white"),
            "accent":  (COLORS["accent"], "#246e78", "white"),
        }
        bg, hover_bg, fg = colors_map.get(variant, colors_map["primary"])

        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            font=FONTS["button"],
            relief="flat",
            cursor="hand2",
            width=width,
            pady=8,
            borderwidth=0,
            **kwargs
        )
        self._bg = bg
        self._hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self._hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


class Card(tk.Frame):
    """A 'card' with subtle border, used to group form fields."""
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs
        )


class Header(tk.Frame):
    """Page header strip with title + back button."""
    def __init__(self, parent, title, on_back=None):
        super().__init__(parent, bg=COLORS["primary"], height=70)
        self.pack_propagate(False)

        if on_back:
            back_btn = tk.Button(
                self, text="← Back", command=on_back,
                bg=COLORS["primary"], fg="white",
                activebackground=COLORS["primary_hover"],
                activeforeground="white",
                font=FONTS["body_bold"],
                relief="flat", cursor="hand2", borderwidth=0
            )
            back_btn.pack(side="left", padx=PAD_M, pady=PAD_M)

        title_lbl = tk.Label(
            self, text=title,
            bg=COLORS["primary"], fg="white",
            font=FONTS["heading"]
        )
        title_lbl.pack(side="left", padx=PAD_M, pady=PAD_M)


def setup_treeview_style():
    """Style ttk.Treeview to match our theme. Call once at app start."""
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface"],
        rowheight=28,
        font=FONTS["body"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["primary"],
        foreground="white",
        font=FONTS["body_bold"],
        relief="flat",
        padding=8,
    )
    style.map("Treeview.Heading",
              background=[("active", COLORS["primary_hover"])])
    style.map("Treeview",
              background=[("selected", COLORS["accent"])],
              foreground=[("selected", "white")])


class LabeledEntry(tk.Frame):
    """A label + entry box pair, stacked vertically."""
    def __init__(self, parent, label_text, width=30, show=None):
        super().__init__(parent, bg=COLORS["surface"])
        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["body_bold"], anchor="w"
        ).pack(fill="x", pady=(0, 2))
        self.entry = tk.Entry(
            self, width=width, font=FONTS["body"],
            relief="solid", borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["primary"],
        )
        if show:
            self.entry.config(show=show)
        self.entry.pack(fill="x", ipady=5)

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value) if value is not None else "")


class LabeledCombobox(tk.Frame):
    """A label + dropdown pair. Used for foreign key selection (shows names, stores IDs)."""
    def __init__(self, parent, label_text, options=None):
        """
        options: list of tuples (id, display_name).
        e.g. [(1, "Cardiology"), (2, "Pediatrics")]
        """
        super().__init__(parent, bg=COLORS["surface"])
        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["body_bold"], anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self._id_map = {}   # display name -> id
        self._reverse = {}  # id -> display name
        self.combo = ttk.Combobox(self, font=FONTS["body"], state="readonly")
        self.combo.pack(fill="x", ipady=3)
        if options:
            self.set_options(options)

    def set_options(self, options):
        """options: list of (id, display_name) tuples."""
        self._id_map = {name: id_ for id_, name in options}
        self._reverse = {id_: name for id_, name in options}
        self.combo["values"] = list(self._id_map.keys())

    def get_id(self):
        """Returns the selected id (not the display name), or None."""
        name = self.combo.get()
        return self._id_map.get(name)

    def set_by_id(self, id_):
        name = self._reverse.get(id_)
        if name:
            self.combo.set(name)

    def clear(self):
        self.combo.set("")
