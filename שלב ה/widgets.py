"""
Reusable styled widgets.
Use these instead of raw tk.Button etc. to keep the UI consistent.
"""

import tkinter as tk
from tkinter import ttk
from styles import COLORS, FONTS, PAD_XS, PAD_S, PAD_M, PAD_L, BTN_PADY


class StyledButton(tk.Frame):
    """A modern, rounded-feel button built from a Frame + Label for macOS compatibility."""

    VARIANTS = {
        "primary": {
            "bg": COLORS["primary"], "hover": COLORS["primary_hover"],
            "active": "#312E81", "fg": "#FFFFFF",
        },
        "success": {
            "bg": COLORS["success"], "hover": "#047857",
            "active": "#065F46", "fg": "#FFFFFF",
        },
        "danger": {
            "bg": COLORS["danger"], "hover": "#B91C1C",
            "active": "#991B1B", "fg": "#FFFFFF",
        },
        "warning": {
            "bg": COLORS["warning"], "hover": "#B45309",
            "active": "#92400E", "fg": "#FFFFFF",
        },
        "accent": {
            "bg": COLORS["accent"], "hover": COLORS["accent_hover"],
            "active": "#075985", "fg": "#FFFFFF",
        },
        "ghost": {
            "bg": COLORS["surface"], "hover": COLORS["border_light"],
            "active": COLORS["border"], "fg": COLORS["text"],
        },
    }

    def __init__(self, parent, text, command=None, variant="primary", width=18, **kwargs):
        v = self.VARIANTS.get(variant, self.VARIANTS["primary"])
        super().__init__(parent, bg=v["bg"], cursor="hand2", **kwargs)

        self._bg = v["bg"]
        self._hover_bg = v["hover"]
        self._active_bg = v["active"]
        self._fg = v["fg"]
        self._command = command
        self._mouse_inside = False
        self._state = "normal"

        self.label = tk.Label(
            self, text=text,
            bg=v["bg"], fg=v["fg"],
            font=FONTS["button"],
            width=width,
            pady=BTN_PADY,
            anchor="center",
        )
        self.label.pack(fill="both", expand=True)

        # Bind on both frame and label
        for w in (self, self.label):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._on_click)
            w.bind("<ButtonRelease-1>", self._on_release)

    def set_state(self, state):
        self._state = state
        if state == "disabled":
            self.config(bg=COLORS["border"])
            self.label.config(bg=COLORS["border"], fg=COLORS["text_muted"], cursor="arrow")
            self.config(cursor="arrow")
        else:
            self.config(bg=self._bg, cursor="hand2")
            self.label.config(bg=self._bg, fg=self._fg, cursor="hand2")

    def config(self, **kw):
        # Forward width to label if provided
        if "width" in kw:
            self.label.config(width=kw.pop("width"))
        super().config(**kw)

    def _set_bg(self, color):
        super().config(bg=color)
        self.label.config(bg=color)

    def _on_enter(self, event):
        if self._state == "disabled":
            return
        self._mouse_inside = True
        self._set_bg(self._hover_bg)

    def _on_leave(self, event):
        if self._state == "disabled":
            return
        self._mouse_inside = False
        self._set_bg(self._bg)

    def _on_click(self, event):
        if self._state == "disabled":
            return
        self._set_bg(self._active_bg)

    def _on_release(self, event):
        if self._state == "disabled":
            return
        self._set_bg(self._hover_bg if self._mouse_inside else self._bg)
        if self._mouse_inside and self._command:
            self._command()


class Card(tk.Frame):
    """A clean card container with subtle shadow-like border."""
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=0, pady=0,
            **kwargs,
        )


class StatCard(tk.Frame):
    """A compact KPI metric card with colored accent bar."""
    def __init__(self, parent, title, value, color_accent=None, **kwargs):
        super().__init__(parent, bg=COLORS["surface"],
                         highlightbackground=COLORS["border"], highlightthickness=1,
                         **kwargs)

        inner = tk.Frame(self, bg=COLORS["surface"])
        inner.pack(fill="both", expand=True, padx=PAD_M, pady=PAD_M)

        if color_accent:
            bar = tk.Frame(inner, bg=color_accent, width=4)
            bar.pack(side="left", fill="y", padx=(0, PAD_M))

        text_box = tk.Frame(inner, bg=COLORS["surface"])
        text_box.pack(side="left", fill="both", expand=True)

        self.value_lbl = tk.Label(
            text_box, text=value,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("Helvetica Neue", 22, "bold"), anchor="w",
        )
        self.value_lbl.pack(fill="x")

        self.title_lbl = tk.Label(
            text_box, text=title,
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["small"], anchor="w",
        )
        self.title_lbl.pack(fill="x", pady=(2, 0))

    def update_value(self, new_val):
        self.value_lbl.config(text=new_val)


class Header(tk.Frame):
    """Full-width page header strip."""
    def __init__(self, parent, title, on_back=None):
        super().__init__(parent, bg=COLORS["primary"], height=56)
        self.pack_propagate(False)

        if on_back:
            back = tk.Label(
                self, text="←  Back",
                bg=COLORS["primary"], fg="#C7D2FE",
                font=FONTS["body_bold"], cursor="hand2",
                padx=PAD_M,
            )
            back.pack(side="left", padx=(PAD_S, 0), pady=PAD_S)
            back.bind("<Button-1>", lambda e: on_back())
            back.bind("<Enter>", lambda e: back.config(fg="#FFFFFF"))
            back.bind("<Leave>", lambda e: back.config(fg="#C7D2FE"))

        tk.Label(
            self, text=title,
            bg=COLORS["primary"], fg="#FFFFFF",
            font=FONTS["heading"],
        ).pack(side="left", padx=PAD_M, pady=PAD_S)


class LabeledEntry(tk.Frame):
    """Label + entry pair with modern focus ring."""
    def __init__(self, parent, label_text, width=30, show=None):
        super().__init__(parent, bg=COLORS["surface"])

        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=FONTS["small_bold"], anchor="w",
        ).pack(fill="x", pady=(0, 3))

        self.ring = tk.Frame(self, bg=COLORS["input_border"], padx=1, pady=1)
        self.ring.pack(fill="x")

        self.entry = tk.Entry(
            self.ring, width=width, font=FONTS["body"],
            relief="flat",
            bg=COLORS["input_bg"], fg=COLORS["text"],
            insertbackground=COLORS["text"],
        )
        if show:
            self.entry.config(show=show)
        self.entry.pack(fill="x", ipady=6, padx=1, pady=1)

        self.entry.bind("<FocusIn>", lambda e: self.ring.config(bg=COLORS["input_focus"]))
        self.entry.bind("<FocusOut>", lambda e: self.ring.config(bg=COLORS["input_border"]))

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        old_state = self.entry.cget("state")
        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value) if value is not None else "")
        self.entry.config(state=old_state)


class LabeledCombobox(tk.Frame):
    """Label + dropdown pair for FK selection."""
    def __init__(self, parent, label_text, options=None, on_change=None):
        super().__init__(parent, bg=COLORS["surface"])

        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=FONTS["small_bold"], anchor="w",
        ).pack(fill="x", pady=(0, 3))

        self._id_map = {}
        self._reverse = {}
        self.on_change = on_change

        self.ring = tk.Frame(self, bg=COLORS["input_border"], padx=1, pady=1)
        self.ring.pack(fill="x")

        self.combo = ttk.Combobox(self.ring, font=FONTS["body"], state="readonly", height=15)
        self.combo.pack(fill="x", ipady=4)

        self.combo.bind("<FocusIn>", lambda e: self.ring.config(bg=COLORS["input_focus"]))
        self.combo.bind("<FocusOut>", lambda e: self.ring.config(bg=COLORS["input_border"]))
        self.combo.bind("<<ComboboxSelected>>", self._handle_select)

        if options:
            self.set_options(options)

    def _handle_select(self, event):
        if self.on_change:
            self.on_change(self.get_id())

    def set_options(self, options):
        """options: list of (id, display_name) tuples."""
        self._id_map = {name: id_ for id_, name in options}
        self._reverse = {id_: name for id_, name in options}
        self.combo["values"] = list(self._id_map.keys())

    def get_id(self):
        name = self.combo.get()
        return self._id_map.get(name)

    def set_by_id(self, id_):
        name = self._reverse.get(id_)
        if name:
            self.combo.set(name)

    def clear(self):
        self.combo.set("")


def setup_treeview_style():
    """Style ttk widgets globally. Call once at startup."""
    style = ttk.Style()
    style.theme_use("clam")

    # ── Treeview ──
    style.configure(
        "Treeview",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface"],
        rowheight=32,
        font=FONTS["body"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["primary"],
        foreground="#FFFFFF",
        font=FONTS["small_bold"],
        relief="flat",
        padding=8,
    )
    style.map("Treeview.Heading", background=[("active", COLORS["primary_hover"])])
    style.map(
        "Treeview",
        background=[("selected", COLORS["primary_light"])],
        foreground=[("selected", COLORS["primary"])],
    )

    # ── Notebook (Tabs) ──
    style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COLORS["surface"],
        foreground=COLORS["text_muted"],
        font=FONTS["body_bold"],
        padding=[20, 10],
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["primary"]), ("active", COLORS["primary_light"])],
        foreground=[("selected", "#FFFFFF"), ("active", COLORS["primary"])],
    )

    # ── Combobox ──
    style.configure(
        "TCombobox",
        arrowcolor=COLORS["text_muted"],
        background=COLORS["surface"],
        fieldbackground=COLORS["surface"],
        foreground=COLORS["text"],
        relief="flat",
        borderwidth=1,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORS["surface"]), ("focus", COLORS["surface"])],
        background=[("readonly", COLORS["surface"])],
    )

    # ── Scrollbar ──
    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["border"],
        troughcolor=COLORS["surface_alt"],
        borderwidth=0,
        arrowsize=0,
        width=8,
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", COLORS["divider"])],
    )
