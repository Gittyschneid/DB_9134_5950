# Stage 5 – Graphical User Interface

GUI application for the Hospital Medical Staff Management System.

**Authors:** Gitty Schneider (333805950) & Avital Tal (214939134)

---

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL running with the database from Stages 1–4
- `psycopg2-binary` package

## 🚀 Setup & Run

### 1. Install dependencies

```bash
pip install psycopg2-binary
```

### 2. Configure the database connection

Open **`db.py`** and update the `DB_CONFIG` dictionary with your credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "hospital_db",   # your DB name
    "user": "postgres",          # your username
    "password": "your_password"  # your password
}
```

### 3. Configure the function/procedure names (if needed)

Open **`screens/procedures_screen.py`** and verify the names match your Stage 4 code:

- Line ~95: `"get_underutilized_staff_count"` — change to your function's actual name
- Line ~160: `"transfer_patient"` — change to your procedure's actual name

### 4. Run the application

```bash
python main.py
```

---

## 🗂️ Project Structure

```
stage5/
├── main.py                  # Entry point - login/menu screen
├── db.py                    # Database connection layer
├── styles.py                # Colors, fonts, spacing constants
├── widgets.py               # Reusable styled widgets
├── README.md                # This file
└── screens/
    ├── __init__.py
    ├── crud_base.py         # Generic CRUD screen (the base class)
    ├── staff_screen.py      # Staff / Doctor / Nurse tabs
    ├── department_screen.py # Department CRUD
    ├── shift_screen.py      # Shift / Staff_Shift tabs
    ├── queries_screen.py    # Runs Stage 2 SELECT queries
    └── procedures_screen.py # Runs Stage 4 functions/procedures
```

## 🎯 Features

### Screens
- **Main Menu** – central navigation with connection status indicator
- **Staff Management** – CRUD for Staff, Doctors, and Nurses (3 tabs)
- **Departments** – CRUD for departments
- **Shifts & Assignments** – CRUD for Shifts and Staff_Shift (2 tabs)
- **Reports & Queries** – runs 2 of the Stage 2 SELECT queries:
  - Monthly Workload Report
  - Understaffed Departments
- **Procedures & Functions** – runs 2 of the Stage 4 PL/pgSQL programs:
  - Function: `get_underutilized_staff_count`
  - Procedure: `transfer_patient`

### CRUD operations (on every table screen)
- **Insert** – fill the form, click Insert
- **Update** – enter the primary key, click "Load Record" to fetch existing data, edit, click Update
- **Delete** – enter the primary key, click Delete (with confirmation)
- **Read** – data table on the right refreshes automatically; click any row to load it into the form

### UX details (per Stage 5 requirements)
- **No raw IDs are shown** — foreign keys are displayed as the related entity's name (e.g. "Cardiology" instead of department_id = 5)
- **FK dropdowns** — when selecting a department, role, etc., users pick from a dropdown of names
- **Update workflow** — user enters the PK and the system fetches the rest, just like the spec requires

---

## 🛠️ How the code is organized (for the report)

The codebase uses a **generic CRUD base class** (`crud_base.py`) that handles all the shared logic for table screens. Each table-specific screen then just declares its configuration:

```python
class DepartmentScreen(CRUDScreen):
    TABLE = "department"
    TITLE = "Department Management"
    PRIMARY_KEY = "department_id"
    FIELDS = [...]
    DISPLAY_QUERY = "SELECT ... ORDER BY ..."
```

This means:
- The same proven CRUD logic is reused across all 7+ tables (less bugs)
- Adding a new table is fast — just write the configuration
- Foreign keys are declared declaratively: `{"type": "fk", "fk_table": "department", "fk_display": "department_name"}` automatically becomes a dropdown showing names

## 🧰 Tools used

- **Python 3** – language
- **Tkinter / ttk** – GUI framework (standard library, no external GUI deps)
- **psycopg2** – PostgreSQL driver
- **PostgreSQL** – database (from Stages 1–4)

## 🐛 Troubleshooting

**"Database error" on the home screen**
- Check that PostgreSQL is running
- Verify the credentials in `db.py`
- Verify your database name matches

**"Function does not exist" when clicking a procedure button**
- Open `screens/procedures_screen.py` and update the function/procedure names to match what you actually created in PostgreSQL during Stage 4

**Combobox is empty (FK dropdown has no options)**
- This means the FK table is empty or the column names in `fk_key`/`fk_display` don't match. Check the table actually has rows and the column names are correct.

**Tkinter not installed (Linux)**
```bash
sudo apt-get install python3-tk
```
