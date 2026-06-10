"""
Procedures and Functions screen.
Runs PL/pgSQL programs from Stage 4.

IMPORTANT: Update the function/procedure NAMES and PARAMETER NAMES below
to match exactly what you defined in PostgreSQL in Stage 4!
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS, PAD_S, PAD_M, PAD_L
from widgets import StyledButton, Card, Header, LabeledEntry
from db import call_function, call_procedure


class ProceduresScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        Header(self, title="Procedures & Functions", on_back=app.show_home).pack(fill="x")

        # Use notebook for clear organization
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        notebook.add(self._build_function_panel(notebook), text="📈 Function: Under-utilized Staff")
        notebook.add(self._build_procedure_panel(notebook), text="🔄 Procedure: Transfer Patient")

    # =========================================================
    # FUNCTION 1: get number of under-utilized staff
    # =========================================================
    def _build_function_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])

        card = Card(frame)
        card.pack(fill="x", padx=PAD_L, pady=PAD_L, ipadx=PAD_L, ipady=PAD_M)

        tk.Label(
            card, text="Under-utilized Staff Counter",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"]
        ).pack(anchor="w", padx=PAD_M, pady=(PAD_S, PAD_S))

        tk.Label(
            card,
            text="Returns the number of staff members who worked at or below the given shift threshold.\n"
                 "Useful for identifying under-utilized human resources.",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"], justify="left"
        ).pack(anchor="w", padx=PAD_M, pady=(0, PAD_M))

        # Parameters
        param_frame = tk.Frame(card, bg=COLORS["surface"])
        param_frame.pack(anchor="w", padx=PAD_M, pady=PAD_S)

        self.threshold_entry = LabeledEntry(param_frame, "Shift threshold (e.g. 1)", width=15)
        self.threshold_entry.pack(side="left", padx=PAD_S)
        self.threshold_entry.set("1")

        StyledButton(
            param_frame, text="▶  Run Function",
            command=self.run_function, variant="success", width=18
        ).pack(side="left", padx=PAD_M)

        # Result
        self.func_result_label = tk.Label(
            frame, text="",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["heading"]
        )
        self.func_result_label.pack(pady=PAD_L)

        # Detail table
        self.func_tree = ttk.Treeview(frame, show="headings", height=15)
        self.func_tree.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        return frame

    def run_function(self):
        try:
            threshold = int(self.threshold_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Threshold must be a number.")
            return

        try:
            # 🔧 UPDATE function name to match your Stage 4 function!
            result = call_function("get_underutilized_staff_count", (threshold,))
        except Exception as e:
            messagebox.showerror("Function Error",
                f"Error calling function. Check the function name in procedures_screen.py "
                f"matches your Stage 4 function name.\n\nDetails:\n{e}")
            return

        if result and len(result) > 0:
            # function returns a scalar - get the first column of first row
            first_row = result[0]
            value = list(first_row.values())[0]
            self.func_result_label.config(
                text=f"✓  {value} staff members worked ≤ {threshold} shift(s)",
                fg=COLORS["success"]
            )
        else:
            self.func_result_label.config(text="(no result)", fg=COLORS["text_muted"])

    # =========================================================
    # PROCEDURE 1: Transfer a patient between staff members
    # =========================================================
    def _build_procedure_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])

        card = Card(frame)
        card.pack(fill="x", padx=PAD_L, pady=PAD_L, ipadx=PAD_L, ipady=PAD_M)

        tk.Label(
            card, text="Transfer Patient Assignment",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"]
        ).pack(anchor="w", padx=PAD_M, pady=(PAD_S, PAD_S))

        tk.Label(
            card,
            text="Reassigns a patient from one staff member to another.\n"
                 "Useful for clinical handoffs and workload balancing.",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"], justify="left"
        ).pack(anchor="w", padx=PAD_M, pady=(0, PAD_M))

        # Parameters
        param_frame = tk.Frame(card, bg=COLORS["surface"])
        param_frame.pack(anchor="w", padx=PAD_M, pady=PAD_M)

        self.patient_id_entry = LabeledEntry(param_frame, "Patient ID", width=15)
        self.patient_id_entry.grid(row=0, column=0, padx=PAD_S, pady=PAD_S)

        self.from_staff_entry = LabeledEntry(param_frame, "From Staff ID", width=15)
        self.from_staff_entry.grid(row=0, column=1, padx=PAD_S, pady=PAD_S)

        self.to_staff_entry = LabeledEntry(param_frame, "To Staff ID", width=15)
        self.to_staff_entry.grid(row=0, column=2, padx=PAD_S, pady=PAD_S)

        StyledButton(
            card, text="▶  Run Procedure",
            command=self.run_procedure, variant="warning", width=18
        ).pack(anchor="w", padx=PAD_M, pady=PAD_M)

        # Status area
        self.proc_status = tk.Label(
            frame, text="",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["body_bold"], wraplength=900, justify="left"
        )
        self.proc_status.pack(pady=PAD_L, padx=PAD_L, anchor="w")

        return frame

    def run_procedure(self):
        try:
            patient_id  = int(self.patient_id_entry.get())
            from_staff  = int(self.from_staff_entry.get())
            to_staff    = int(self.to_staff_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "All IDs must be numbers.")
            return

        try:
            # 🔧 UPDATE procedure name + parameter order to match your Stage 4 procedure!
            call_procedure("transfer_patient", (patient_id, from_staff, to_staff))
            self.proc_status.config(
                text=f"✓  Patient {patient_id} successfully transferred "
                     f"from staff {from_staff} to staff {to_staff}.",
                fg=COLORS["success"]
            )
        except Exception as e:
            self.proc_status.config(
                text=f"✗  Error: {e}\n\nMake sure the procedure name and parameter "
                     f"order in procedures_screen.py match your Stage 4 procedure.",
                fg=COLORS["danger"]
            )
