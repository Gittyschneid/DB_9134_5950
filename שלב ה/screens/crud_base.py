"""
Generic CRUD screen.
Subclass this for each table - just provide table_name, fields, and FK config.
This is what makes the app DRY (Don't Repeat Yourself).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS, PAD_XS, PAD_S, PAD_M, PAD_L
from widgets import StyledButton, Card, Header, LabeledEntry, LabeledCombobox
from db import run_query, run_action


class CRUDScreen(tk.Frame):
    """
    Base class for any table CRUD screen.

    Subclass configuration:
        TABLE       = "staff"
        TITLE       = "Staff Management"
        PRIMARY_KEY = "staff_id"
        FIELDS      = [ {"col": "first_name", "label": "First Name", "type": "text"}, ... ]
        DISPLAY_QUERY = "SELECT ... FROM ..."
    """

    TABLE = None
    TITLE = "CRUD"
    PRIMARY_KEY = "id"
    FIELDS = []
    DISPLAY_QUERY = None

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.entries = {}
        self.record_loaded = False
        self.insert_mode = False

        # Header
        Header(self, title=self.TITLE, on_back=app.show_home).pack(fill="x")

        # Body: left form + right table
        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        self._build_form(body)
        self._build_table(body)

        self._load_fk_options()
        self.refresh_table()
        self.update_button_visibility()

    # ── FORM (left) ──────────────────────────────────────────────
    def _build_form(self, parent):
        form_card = Card(parent)
        form_card.pack(side="left", fill="y", padx=(0, PAD_M), ipadx=PAD_M, ipady=PAD_M)

        # Title
        tk.Label(
            form_card, text=self.TITLE,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"],
        ).pack(pady=(PAD_M, PAD_S), padx=PAD_M)

        # PK field
        pk_label = self.PRIMARY_KEY.replace("_", " ").title() + "  (Primary Key)"
        pk_entry = LabeledEntry(form_card, pk_label, width=26)
        pk_entry.pack(pady=PAD_XS, padx=PAD_M, fill="x")
        self.entries[self.PRIMARY_KEY] = pk_entry

        # Top action buttons (Search + Insert)
        top_btns = tk.Frame(form_card, bg=COLORS["surface"])
        top_btns.pack(pady=(PAD_S, PAD_S), padx=PAD_M, fill="x")

        self.btn_search = StyledButton(
            top_btns, text="Search", command=self.load_by_pk,
            variant="accent", width=12,
        )
        self.btn_search.pack(side="left", padx=(0, PAD_XS), expand=True, fill="x")

        self.btn_insert = StyledButton(
            top_btns, text="Insert", command=self.show_insert_form,
            variant="success", width=12,
        )
        self.btn_insert.pack(side="left", padx=(PAD_XS, 0), expand=True, fill="x")

        # Divider
        tk.Frame(form_card, bg=COLORS["border"], height=1).pack(
            fill="x", padx=PAD_M, pady=PAD_S,
        )

        # ── Fields container (hidden until needed) ──
        self.fields_frame = tk.Frame(form_card, bg=COLORS["surface"])

        for f in self.FIELDS:
            if f["type"] == "fk":
                widget = LabeledCombobox(self.fields_frame, f["label"])
            else:
                widget = LabeledEntry(self.fields_frame, f["label"], width=26)
            widget.pack(pady=PAD_XS, padx=PAD_M, fill="x")
            self.entries[f["col"]] = widget

        # Action buttons inside fields container
        self.btn_frame = tk.Frame(self.fields_frame, bg=COLORS["surface"])
        self.btn_frame.pack(pady=(PAD_M, PAD_S), padx=PAD_M, fill="x")

        self.btn_save   = StyledButton(self.btn_frame, "Save",   self.save_insert_record, variant="success", width=10)
        self.btn_cancel = StyledButton(self.btn_frame, "Cancel", self.clear_form,         variant="ghost",   width=10)
        self.btn_update = StyledButton(self.btn_frame, "Update", self.update_record,      variant="warning", width=8)
        self.btn_delete = StyledButton(self.btn_frame, "Delete", self.delete_record,      variant="danger",  width=8)
        self.btn_clear  = StyledButton(self.btn_frame, "Clear",  self.clear_form,         variant="ghost",   width=8)

    # ── TABLE (right) ────────────────────────────────────────────
    def _build_table(self, parent):
        right = tk.Frame(parent, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right, text="Records  (click a row to edit)",
            bg=COLORS["bg"], fg=COLORS["text_secondary"],
            font=FONTS["small_bold"],
        ).pack(anchor="w", pady=(0, PAD_XS))

        table_frame = tk.Frame(right, bg=COLORS["surface"],
                               highlightbackground=COLORS["border"], highlightthickness=1)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, show="headings")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        StyledButton(
            right, text="Refresh", command=self.refresh_table,
            variant="ghost", width=12,
        ).pack(pady=(PAD_S, 0), anchor="e")

    # ── FK options ───────────────────────────────────────────────
    def _load_fk_options(self):
        for f in self.FIELDS:
            if f["type"] != "fk":
                continue
            try:
                rows = run_query(
                    f"SELECT {f['fk_key']} AS id, {f['fk_display']} AS name "
                    f"FROM {f['fk_table']} ORDER BY {f['fk_display']}"
                )
                self.entries[f["col"]].set_options([(r["id"], r["name"]) for r in rows])
            except Exception as e:
                messagebox.showwarning("FK load failed", f"Could not load {f['label']}:\n{e}")

    # ── CRUD operations ─────────────────────────────────────────
    def refresh_table(self):
        try:
            rows = run_query(self.DISPLAY_QUERY)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not rows:
            self.tree["columns"] = ("info",)
            self.tree.heading("info", text="No records found")
            return

        cols = list(rows[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=120, anchor="w")

        for r in rows:
            self.tree.insert("", "end", values=[r[c] for c in cols])

    def _on_row_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        if values:
            self.entries[self.PRIMARY_KEY].set(values[0])
            self.load_by_pk()

    # ── Button visibility ────────────────────────────────────────
    def update_button_visibility(self):
        for btn in (self.btn_save, self.btn_cancel, self.btn_update, self.btn_delete, self.btn_clear):
            btn.pack_forget()

        pk_widget = self.entries.get(self.PRIMARY_KEY)

        if self.insert_mode:
            self.fields_frame.pack(fill="x")
            if pk_widget:
                pk_widget.entry.config(state="normal")
            self.btn_search.set_state("disabled")
            self.btn_insert.set_state("disabled")
            self.btn_save.pack(side="left", padx=(0, PAD_XS), expand=True, fill="x")
            self.btn_cancel.pack(side="left", padx=(PAD_XS, 0), expand=True, fill="x")

        elif self.record_loaded:
            self.fields_frame.pack(fill="x")
            if pk_widget:
                pk_widget.entry.config(state="disabled")
            self.btn_search.set_state("normal")
            self.btn_insert.set_state("disabled")
            self.btn_update.pack(side="left", padx=(0, PAD_XS), expand=True, fill="x")
            self.btn_delete.pack(side="left", padx=PAD_XS, expand=True, fill="x")
            self.btn_clear.pack(side="left", padx=(PAD_XS, 0), expand=True, fill="x")

        else:
            self.fields_frame.pack_forget()
            if pk_widget:
                pk_widget.entry.config(state="normal")
            self.btn_search.set_state("normal")
            self.btn_insert.set_state("normal")

    # ── Load record ──────────────────────────────────────────────
    def load_by_pk(self):
        pk_value = self.entries[self.PRIMARY_KEY].get()
        if not pk_value:
            messagebox.showwarning("Missing", f"Please enter a value for {self.PRIMARY_KEY.replace('_', ' ').title()}.")
            return
        try:
            rows = run_query(
                f"SELECT * FROM {self.TABLE} WHERE {self.PRIMARY_KEY} = %s",
                (pk_value,),
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not rows:
            messagebox.showinfo("Not found", f"No record with {self.PRIMARY_KEY.replace('_', ' ').title()} = {pk_value}")
            self.record_loaded = False
            self.update_button_visibility()
            return

        self.record_loaded = True
        self.insert_mode = False
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

    # ── Insert flow ──────────────────────────────────────────────
    def show_insert_form(self):
        for col, widget in self.entries.items():
            if hasattr(widget, "set"):
                widget.set("")
            elif hasattr(widget, "clear"):
                widget.clear()
        self.record_loaded = False
        self.insert_mode = True
        self.update_button_visibility()

    def save_insert_record(self):
        pk_value = self.entries[self.PRIMARY_KEY].get()
        if not pk_value:
            messagebox.showwarning("Missing", f"Please enter a value for {self.PRIMARY_KEY.replace('_', ' ').title()}.")
            return
        data = self._collect_values(include_pk=True)
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

    # ── Update ───────────────────────────────────────────────────
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

    # ── Delete ───────────────────────────────────────────────────
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

    # ── Clear ────────────────────────────────────────────────────
    def clear_form(self):
        for col, widget in self.entries.items():
            if hasattr(widget, "set"):
                widget.set("")
            elif hasattr(widget, "clear"):
                widget.clear()
        self.record_loaded = False
        self.insert_mode = False
        self.update_button_visibility()
