"""
Reusable styled widgets.
Use these instead of raw tk.Button etc. to keep the UI consistent.
"""

import tkinter as tk
from tkinter import ttk
from styles import COLORS, FONTS, PAD_S, PAD_M, PAD_L


class StyledButton(tk.Label):
    """A custom label-based button that works perfectly on all OSes, especially macOS."""
    def __init__(self, parent, text, command=None, variant="primary", width=18, **kwargs):
        colors_map = {
            "primary": (COLORS["primary"], COLORS["primary_hover"], "#312E81", "white"),  # bg, hover, active, fg
            "success": (COLORS["success"], "#059669", "#047857", "white"),
            "danger":  (COLORS["danger"], "#DC2626", "#B91C1C", "white"),
            "warning": (COLORS["warning"], "#D97706", "#B45309", "white"),
            "accent":  (COLORS["accent"], "#0284C7", "#0369A1", "white"),
        }
        bg, hover_bg, active_bg, fg = colors_map.get(variant, colors_map["primary"])

        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=FONTS["button"],
            relief="flat",
            cursor="hand2",
            width=width,
            pady=10,
            anchor="center",
            **kwargs
        )
        self._bg = bg
        self._hover_bg = hover_bg
        self._active_bg = active_bg
        self._fg = fg
        self._command = command
        self._mouse_inside = False
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, event):
        self._mouse_inside = True
        self.config(bg=self._hover_bg)

    def _on_leave(self, event):
        self._mouse_inside = False
        self.config(bg=self._bg)

    def _on_click(self, event):
        self.config(bg=self._active_bg)

    def _on_release(self, event):
        self.config(bg=self._hover_bg if self._mouse_inside else self._bg)
        if self._mouse_inside and self._command:
            self._command()


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


class StatCard(Card):
    """A card that displays a single KPI metric (value + title) with a colored indicator."""
    def __init__(self, parent, title, value, color_accent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(padx=PAD_M, pady=PAD_M)
        
        # Accent indicator line on the left
        if color_accent:
            accent_bar = tk.Frame(self, bg=color_accent, width=4)
            accent_bar.pack(side="left", fill="y", padx=(0, PAD_M))
            
        text_container = tk.Frame(self, bg=COLORS["surface"])
        text_container.pack(side="left", fill="both", expand=True)
        
        self.value_lbl = tk.Label(
            text_container, text=value,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=("SF Pro Text", 20, "bold"), anchor="w"
        )
        self.value_lbl.pack(fill="x")
        
        self.title_lbl = tk.Label(
            text_container, text=title,
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["small"], anchor="w"
        )
        self.title_lbl.pack(fill="x", pady=(2, 0))
        
    def update_value(self, new_val):
        self.value_lbl.config(text=new_val)


class Header(tk.Frame):
    """Page header strip with title + back button."""
    def __init__(self, parent, title, on_back=None):
        super().__init__(parent, bg=COLORS["primary"], height=70)
        self.pack_propagate(False)

        if on_back:
            # Custom back button styled with high-contrast label-based button
            back_btn = StyledButton(
                self, text="← Back", command=on_back,
                variant="primary", width=8
            )
            back_btn.pack(side="left", padx=PAD_M, pady=PAD_M)

        title_lbl = tk.Label(
            self, text=title,
            bg=COLORS["primary"], fg="white",
            font=FONTS["heading"]
        )
        title_lbl.pack(side="left", padx=PAD_M, pady=PAD_M)


def setup_treeview_style():
    """Style ttk.Treeview, Notebook, and Combobox. Call once at app start."""
    style = ttk.Style()
    style.theme_use("clam")  # Clam supports more custom color options than default

    # Treeview styles
    style.configure(
        "Treeview",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface"],
        rowheight=30,
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

    # Notebook (Tabs) style
    style.configure(
        "TNotebook",
        background=COLORS["bg"],
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        background=COLORS["border"],
        foreground=COLORS["text_muted"],
        font=FONTS["body_bold"],
        padding=[16, 8],
        borderwidth=0,
        relief="flat"
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["primary"]), ("active", COLORS["primary_hover"])],
        foreground=[("selected", "white"), ("active", "white")]
    )

    # Combobox style
    style.configure(
        "TCombobox",
        arrowcolor=COLORS["text_muted"],
        background=COLORS["surface"],
        fieldbackground=COLORS["surface"],
        foreground=COLORS["text"],
        relief="flat",
        borderwidth=1,
        bordercolor=COLORS["border"]
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORS["surface"]), ("focus", COLORS["surface"])],
        background=[("readonly", COLORS["surface"])],
        bordercolor=[("focus", COLORS["primary"])]
    )


class LabeledEntry(tk.Frame):
    """A label + entry box pair, stacked vertically with focus outlines."""
    def __init__(self, parent, label_text, width=30, show=None):
        super().__init__(parent, bg=COLORS["surface"])
        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["body_bold"], anchor="w"
        ).pack(fill="x", pady=(0, 2))
        
        # Wrap the entry in a frame to form a custom 1px border ring
        self.entry_frame = tk.Frame(
            self,
            bg=COLORS["border"],
            padx=1, pady=1
        )
        self.entry_frame.pack(fill="x")
        
        self.entry = tk.Entry(
            self.entry_frame, width=width, font=FONTS["body"],
            relief="flat", bg=COLORS["surface"], fg=COLORS["text"],
            insertbackground=COLORS["text"]
        )
        if show:
            self.entry.config(show=show)
        self.entry.pack(fill="x", ipady=5, padx=1, pady=1)
        
        # Focus events for modern styling
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
    def _on_focus_in(self, event):
        self.entry_frame.config(bg=COLORS["primary"])
        
    def _on_focus_out(self, event):
        self.entry_frame.config(bg=COLORS["border"])

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        old_state = self.entry.cget("state")
        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value) if value is not None else "")
        self.entry.config(state=old_state)


class LabeledCombobox(tk.Frame):
    """A label + dropdown pair. Used for foreign key selection."""
    def __init__(self, parent, label_text, options=None):
        super().__init__(parent, bg=COLORS["surface"])
        tk.Label(
            self, text=label_text,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["body_bold"], anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self._id_map = {}   # display name -> id
        self._reverse = {}  # id -> display name
        
        # Wrap combobox to style border on focus
        self.combo_frame = tk.Frame(self, bg=COLORS["border"], padx=1, pady=1)
        self.combo_frame.pack(fill="x")
        
        self.combo = ttk.Combobox(self.combo_frame, font=FONTS["body"], state="readonly")
        self.combo.pack(fill="x", ipady=3)
        
        self.combo.bind("<FocusIn>", lambda e: self.combo_frame.config(bg=COLORS["primary"]))
        self.combo.bind("<FocusOut>", lambda e: self.combo_frame.config(bg=COLORS["border"]))
        
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
