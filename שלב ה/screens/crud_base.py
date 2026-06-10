"""
Generic CRUD screen.
Subclass this for each table - just provide table_name, fields, and FK config.
This is what makes the app DRY (Don't Repeat Yourself).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS, PAD_S, PAD_M, PAD_L
from widgets import StyledButton, Card, Header, LabeledEntry, LabeledCombobox
from db import run_query, run_action


class CRUDScreen(tk.Frame):
    """
    Base class for any table CRUD screen.

    Subclass configuration:
        TABLE      = "staff"                          # actual SQL table name
        TITLE      = "Staff Management"               # shown in header
        PRIMARY_KEY = "staff_id"                      # PK column name
        FIELDS     = [                                # list of fields
            {"col": "first_name", "label": "First Name", "type": "text", "editable_in_insert": True},
            ...
        ]
        # For foreign keys, FIELDS entries look like:
        #   {"col": "department_id", "label": "Department",
        #    "type": "fk", "fk_table": "department",
        #    "fk_key": "department_id", "fk_display": "department_name"}
        DISPLAY_QUERY = "SELECT ... FROM ..."         # SELECT used to populate the table
                                                      # Should JOIN FKs to show names not IDs!
    """

    TABLE = None
    TITLE = "CRUD"
    PRIMARY_KEY = "id"
    FIELDS = []
    DISPLAY_QUERY = None

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.entries = {}  # column_name -> LabeledEntry or LabeledCombobox
        self.record_loaded = False  # Track whether an existing database record is active

        # Header
        Header(self, title=self.TITLE, on_back=app.show_home).pack(fill="x")

        # Body: left = form, right = data table
        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        self._build_form(body)
        self._build_table(body)

        # Load FK options into combos and refresh data
        self._load_fk_options()
        self.refresh_table()
        
        # Apply initial button states
        self.update_button_visibility()

    # ------------------------------------------------------------------
    # FORM (left side)
    # ------------------------------------------------------------------
    def _build_form(self, parent):
        form_card = Card(parent)
        form_card.pack(side="left", fill="y", padx=(0, PAD_L), ipadx=PAD_L, ipady=PAD_L)

        tk.Label(
            form_card, text=self.TITLE,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"]
        ).pack(pady=(PAD_M, PAD_L))

        # PK field (used for update/delete lookup)
        pk_label = self.PRIMARY_KEY.replace("_", " ").title() + " (for Update/Delete)"
        pk_entry = LabeledEntry(form_card, pk_label, width=28)
        pk_entry.pack(pady=PAD_S, padx=PAD_L, fill="x")
        self.entries[self.PRIMARY_KEY] = pk_entry

        load_btn = StyledButton(
            form_card, text="🔎 Load Record",
            command=self.load_by_pk, variant="accent", width=22
        )
        load_btn.pack(pady=(PAD_S, PAD_M), padx=PAD_L)

        # Separator
        tk.Frame(form_card, bg=COLORS["border"], height=1).pack(
            fill="x", padx=PAD_L, pady=PAD_M
        )

        # Other fields
        for f in self.FIELDS:
            if f["type"] == "fk":
                widget = LabeledCombobox(form_card, f["label"])
            else:
                widget = LabeledEntry(form_card, f["label"], width=28)
            widget.pack(pady=PAD_S, padx=PAD_L, fill="x")
            self.entries[f["col"]] = widget

        # Action buttons container
        self.btn_frame = tk.Frame(form_card, bg=COLORS["surface"])
        self.btn_frame.pack(pady=PAD_L, padx=PAD_L, fill="x")

        # Initialize button instances (visibility is handled dynamically)
        self.btn_insert = StyledButton(self.btn_frame, "➕ Insert", self.insert_record, variant="success", width=13)
        self.btn_update = StyledButton(self.btn_frame, "✏️ Update", self.update_record, variant="warning", width=8)
        self.btn_delete = StyledButton(self.btn_frame, "🗑️ Delete", self.delete_record, variant="danger", width=8)
        self.btn_clear = StyledButton(self.btn_frame, "🧹 Clear", self.clear_form, variant="primary", width=8)

    # ------------------------------------------------------------------
    # TABLE (right side)
    # ------------------------------------------------------------------
    def _build_table(self, parent):
        right = tk.Frame(parent, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right, text="Records (click a row to load into form)",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["body_bold"]
        ).pack(anchor="w", pady=(0, PAD_S))

        # Compute display columns from the DISPLAY_QUERY result (first row keys)
        # For now we set placeholder; columns get set on first refresh
        table_frame = tk.Frame(right, bg=COLORS["surface"])
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, show="headings")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        StyledButton(
            right, text="🔄 Refresh", command=self.refresh_table,
            variant="primary", width=15
        ).pack(pady=PAD_M, anchor="e")

    # ------------------------------------------------------------------
    # FK options
    # ------------------------------------------------------------------
    def _load_fk_options(self):
        """For each FK field, fetch (id, display_name) tuples and populate combo."""
        for f in self.FIELDS:
            if f["type"] != "fk":
                continue
            try:
                rows = run_query(
                    f"SELECT {f['fk_key']} AS id, {f['fk_display']} AS name "
                    f"FROM {f['fk_table']} ORDER BY {f['fk_display']}"
                )
                options = [(r["id"], r["name"]) for r in rows]
                self.entries[f["col"]].set_options(options)
            except Exception as e:
                messagebox.showwarning(
                    "FK load failed",
                    f"Could not load options for {f['label']}:\n{e}"
                )

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def refresh_table(self):
        """Reload the data table using DISPLAY_QUERY."""
        try:
            rows = run_query(self.DISPLAY_QUERY)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))
            return

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not rows:
            self.tree["columns"] = ("info",)
            self.tree.heading("info", text="No records found")
            return

        # Set up columns based on first row
        cols = list(rows[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=130, anchor="w")

        for r in rows:
            self.tree.insert("", "end", values=[r[c] for c in cols])

    def _on_row_select(self, event):
        """When a row is clicked, populate the PK field and automatically load the full record."""
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0])["values"]
        if values:
            # Assume the first column in DISPLAY_QUERY is the PK
            self.entries[self.PRIMARY_KEY].set(values[0])
            self.load_by_pk()

    def update_button_visibility(self):
        """Show or hide buttons based on whether a record is currently loaded."""
        # Unpack all buttons from the grid/pack first
        self.btn_insert.pack_forget()
        self.btn_update.pack_forget()
        self.btn_delete.pack_forget()
        self.btn_clear.pack_forget()

        # Update primary key input field state
        pk_widget = self.entries.get(self.PRIMARY_KEY)
        
        if self.record_loaded:
            # We are editing an existing record: Hide Insert, Show Update & Delete, lock PK
            if pk_widget:
                pk_widget.entry.config(state="disabled")
            
            # Use smaller width so 3 buttons fit in one row without expanding the form card
            self.btn_update.config(width=8)
            self.btn_delete.config(width=8)
            self.btn_clear.config(width=8)
            
            self.btn_update.pack(side="left", padx=4)
            self.btn_delete.pack(side="left", padx=4)
            self.btn_clear.pack(side="left", padx=4)
        else:
            # We are in insert mode: Show Insert and Clear, enable PK
            if pk_widget:
                pk_widget.entry.config(state="normal")
                
            self.btn_insert.config(width=13)
            self.btn_clear.config(width=13)
            
            self.btn_insert.pack(side="left", padx=4)
            self.btn_clear.pack(side="left", padx=4)

    def load_by_pk(self):
        """Update flow: user enters PK, system fills the rest of the form."""
        pk_value = self.entries[self.PRIMARY_KEY].get()
        if not pk_value:
            messagebox.showwarning("Missing", f"Please enter {self.PRIMARY_KEY}.")
            return
        try:
            rows = run_query(
                f"SELECT * FROM {self.TABLE} WHERE {self.PRIMARY_KEY} = %s",
                (pk_value,)
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not rows:
            messagebox.showinfo("Not found", f"No record with {self.PRIMARY_KEY} = {pk_value}")
            self.record_loaded = False
            self.update_button_visibility()
            return

        # Successfully loaded the record
        self.record_loaded = True
        self.update_button_visibility()

        row = rows[0]
        for f in self.FIELDS:
            widget = self.entries[f["col"]]
            value = row.get(f["col"])
            if f["type"] == "fk":
                widget.set_by_id(value)
            else:
                widget.set(value)

    def _collect_values(self, include_pk=False):
        """Gather field values from the form into a dict {col: value}."""
        data = {}
        if include_pk:
            v = self.entries[self.PRIMARY_KEY].get()
            if v:
                data[self.PRIMARY_KEY] = v

        for f in self.FIELDS:
            widget = self.entries[f["col"]]
            if f["type"] == "fk":
                val = widget.get_id()
            else:
                val = widget.get()
                if val == "":
                    val = None
            data[f["col"]] = val
        return data

    def insert_record(self):
        data = self._collect_values(include_pk=False)
        cols = list(data.keys())
        placeholders = ", ".join(["%s"] * len(cols))
        col_list = ", ".join(cols)
        query = f"INSERT INTO {self.TABLE} ({col_list}) VALUES ({placeholders})"
        try:
            run_action(query, tuple(data.values()))
            messagebox.showinfo("Success", "Record inserted.")
            self.clear_form()
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Insert Failed", str(e))

    def update_record(self):
        pk_value = self.entries[self.PRIMARY_KEY].get()
        if not pk_value:
            messagebox.showwarning("Missing", f"Enter the {self.PRIMARY_KEY} to update.")
            return
        data = self._collect_values(include_pk=False)
        set_clause = ", ".join([f"{c} = %s" for c in data.keys()])
        query = f"UPDATE {self.TABLE} SET {set_clause} WHERE {self.PRIMARY_KEY} = %s"
        params = tuple(data.values()) + (pk_value,)
        try:
            affected = run_action(query, params)
            if affected == 0:
                messagebox.showinfo("No change", f"No row with {self.PRIMARY_KEY} = {pk_value}")
            else:
                messagebox.showinfo("Success", f"Updated {affected} row(s).")
                self.refresh_table()
        except Exception as e:
            messagebox.showerror("Update Failed", str(e))

    def delete_record(self):
        pk_value = self.entries[self.PRIMARY_KEY].get()
        if not pk_value:
            messagebox.showwarning("Missing", f"Enter the {self.PRIMARY_KEY} to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete record with {self.PRIMARY_KEY} = {pk_value}?"):
            return
        query = f"DELETE FROM {self.TABLE} WHERE {self.PRIMARY_KEY} = %s"
        try:
            affected = run_action(query, (pk_value,))
            if affected == 0:
                messagebox.showinfo("No change", "No matching record found.")
            else:
                messagebox.showinfo("Success", f"Deleted {affected} row(s).")
                self.clear_form()
                self.refresh_table()
        except Exception as e:
            messagebox.showerror("Delete Failed", str(e))

    def clear_form(self):
        for col, widget in self.entries.items():
            if hasattr(widget, "set"):
                widget.set("")
            elif hasattr(widget, "clear"):
                widget.clear()
        self.record_loaded = False
        self.update_button_visibility()
