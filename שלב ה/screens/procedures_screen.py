"""
Procedures and Functions screen.
Runs PL/pgSQL programs from Stage 4.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from styles import COLORS, FONTS, PAD_XS, PAD_S, PAD_M, PAD_L
from widgets import StyledButton, Card, Header, LabeledEntry, LabeledCombobox
from db import call_function, call_procedure, run_query


class ProceduresScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        Header(self, title="Procedures & Functions", on_back=app.show_home).pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        notebook.add(self._build_function_panel(notebook), text="Underworked Staff")
        notebook.add(self._build_procedure_panel(notebook), text="Transfer Patient Assignment")

    # ═══════════════════════════════════════════════════════════
    # FUNCTION: Underworked staff count
    # ═══════════════════════════════════════════════════════════
    def _build_function_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])

        card = Card(frame)
        card.pack(fill="x", padx=PAD_L, pady=PAD_L, ipadx=PAD_L, ipady=PAD_M)

        tk.Label(
            card, text="Underworked Staff Counter",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"],
        ).pack(anchor="w", padx=PAD_M, pady=(PAD_S, PAD_XS))

        tk.Label(
            card,
            text="Returns the number of staff in a department who worked at or below\n"
                 "the minimum shift threshold. Useful for identifying underworked resources.",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"], justify="left",
        ).pack(anchor="w", padx=PAD_M, pady=(0, PAD_M))

        param_frame = tk.Frame(card, bg=COLORS["surface"])
        param_frame.pack(anchor="w", padx=PAD_M, pady=PAD_S)

        self.dept_name_combo = LabeledCombobox(param_frame, "Department Name")
        self.dept_name_combo.pack(side="left", padx=(0, PAD_M))

        try:
            depts = run_query("SELECT department_name FROM department ORDER BY department_name")
            self.dept_name_combo.set_options(
                [(r["department_name"], r["department_name"]) for r in depts]
            )
        except Exception:
            pass

        StyledButton(
            param_frame, text="Run Function",
            command=self.run_function, variant="success", width=16,
        ).pack(side="left", pady=(PAD_M, 0))

        # Result
        self.func_result_label = tk.Label(
            frame, text="",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["heading"],
        )
        self.func_result_label.pack(pady=PAD_L)

        self.func_tree = ttk.Treeview(frame, show="headings", height=12)
        self.func_tree.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))

        return frame

    def run_function(self):
        dept_name = self.dept_name_combo.get_id()
        if not dept_name:
            messagebox.showerror("Missing selection", "Please select a department.")
            return

        try:
            result = call_function("get_underworked_staff_count", (dept_name,))
        except Exception as e:
            messagebox.showerror("Function Error", f"Error calling function.\n\nDetails:\n{e}")
            return

        if result and len(result) > 0:
            value = list(result[0].values())[0]
            self.func_result_label.config(
                text=f"✓  {value} staff members in '{dept_name}' worked ≤ the minimum threshold",
                fg=COLORS["success"],
            )
        else:
            self.func_result_label.config(text="(no result)", fg=COLORS["text_muted"])

    # ═══════════════════════════════════════════════════════════
    # PROCEDURE: Transfer patient assignment
    # ═══════════════════════════════════════════════════════════
    def _build_procedure_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg"])

        card = Card(frame)
        card.pack(fill="x", padx=PAD_L, pady=PAD_L, ipadx=PAD_L, ipady=PAD_M)

        tk.Label(
            card, text="Transfer Patient Assignment",
            bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["subheading"],
        ).pack(anchor="w", padx=PAD_M, pady=(PAD_S, PAD_XS))

        tk.Label(
            card,
            text="Reassigns a patient from one staff member to another.\n"
                 "Useful for clinical handoffs and workload balancing.",
            bg=COLORS["surface"], fg=COLORS["text_muted"],
            font=FONTS["body"], justify="left",
        ).pack(anchor="w", padx=PAD_M, pady=(0, PAD_M))

        param_frame = tk.Frame(card, bg=COLORS["surface"])
        param_frame.pack(anchor="w", padx=PAD_M, pady=PAD_M)

        self.patient_id_combo = LabeledCombobox(
            param_frame, "Patient",
            on_change=self._on_patient_selected
        )
        self.patient_id_combo.grid(row=0, column=0, padx=(0, PAD_S), pady=PAD_XS)

        self.from_staff_combo = LabeledCombobox(param_frame, "From Staff")
        self.from_staff_combo.grid(row=0, column=1, padx=PAD_S, pady=PAD_XS)

        self.to_staff_combo = LabeledCombobox(param_frame, "To Staff")
        self.to_staff_combo.grid(row=0, column=2, padx=(PAD_S, 0), pady=PAD_XS)

        self._load_procedure_options()

        StyledButton(
            card, text="Run Procedure",
            command=self.run_procedure, variant="warning", width=18,
        ).pack(anchor="w", padx=PAD_M, pady=PAD_M)

        self.proc_status = tk.Label(
            frame, text="",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["body_bold"], wraplength=900, justify="left",
        )
        self.proc_status.pack(pady=PAD_L, padx=PAD_L, anchor="w")

        return frame

    def _on_patient_selected(self, patient_id):
        if not patient_id:
            return
        try:
            # Auto-fill the "From Staff" based on the current assignment
            rows = run_query(
                "SELECT staff_id FROM staff_patient_assignment WHERE patient_id = %s",
                (patient_id,)
            )
            if rows:
                self.from_staff_combo.set_by_id(rows[0]["staff_id"])
        except Exception:
            pass

    def _load_procedure_options(self):
        try:
            patients = run_query(
                "SELECT DISTINCT patient_id FROM staff_patient_assignment ORDER BY patient_id"
            )
            self.patient_id_combo.set_options(
                [(r["patient_id"], f"Patient {r['patient_id']}") for r in patients]
            )
        except Exception:
            pass

        try:
            staff = run_query(
                "SELECT staff_id, first_name || ' ' || last_name AS name FROM staff ORDER BY staff_id"
            )
            opts = [(r["staff_id"], f"{r['staff_id']} — {r['name']}") for r in staff]
            self.from_staff_combo.set_options(opts)
            self.to_staff_combo.set_options(opts)
        except Exception:
            pass

    def run_procedure(self):
        patient_id = self.patient_id_combo.get_id()
        from_staff = self.from_staff_combo.get_id()
        to_staff = self.to_staff_combo.get_id()

        if patient_id is None or from_staff is None or to_staff is None:
            messagebox.showerror("Missing selection", "Please select a Patient, From Staff, and To Staff.")
            return

        try:
            # Parameter order matches Stage 4: (old_staff_id, new_staff_id, patient_id_input)
            call_procedure("transfer_patient_assignment", (int(from_staff), int(to_staff), int(patient_id)))
            self.proc_status.config(
                text=f"✓  Patient {patient_id} successfully transferred "
                     f"from staff {from_staff} to staff {to_staff}.",
                fg=COLORS["success"],
            )
        except Exception as e:
            self.proc_status.config(text=f"✗  Error: {e}", fg=COLORS["danger"])
