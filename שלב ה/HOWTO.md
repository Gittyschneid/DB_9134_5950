# Installation & Usage Guide – Hospital Medical Staff Management System

## Prerequisites

- Python 3.8 or higher installed on your machine
- PostgreSQL running with the database from previous stages
- Internet connection for package installation (one time only)

---

## Step 1 – Install Dependencies

Open a terminal (Command Prompt / Terminal) and run:

```bash
pip install psycopg2-binary
```

---

## Step 2 – Configure the Database Connection

Open `db.py` and update the following fields:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,               # your PostgreSQL port
    "database": "hospital_db",  # your database name
    "user": "postgres",         # your username
    "password": "your_password" # your password
}
```

---

## Step 3 – Run the Application

From the project folder, run:

```bash
python main.py
```

The application window will open automatically.

---

## Step 4 – Navigating the System

The home screen displays:
- Database connection status (green = connected)
- Live statistics (total staff, departments, shifts)
- Navigation buttons to all system screens

Click any button to enter the desired screen.

---

## Step 5 – Performing CRUD Operations

On every table screen (Staff, Departments, Shifts, etc.):

| Action | How to perform |
|---|---|
| **Insert** | Fill in the form fields on the left → click Insert |
| **Update** | Enter the record ID in the top field → click Load Record → edit fields → click Update |
| **Delete** | Enter the record ID → click Delete → confirm in the dialog |
| **View** | The table refreshes automatically; click any row to load it into the form |

---

## Step 6 – Running Reports & Queries

1. Click **Analytical Reports** from the main menu
2. Choose one of the two reports:
   - **Monthly Workload Report** – shift count per staff member per month
   - **Understaffed Departments** – departments with insufficient staff
3. Results are displayed in a table directly on the screen

---

## Step 7 – Running Functions & Procedures

1. Click **Procedures & Actions** from the main menu
2. Choose a tab:
   - **Function: Under-utilized Staff** – enter a shift threshold and click Run Function
   - **Procedure: Transfer Patient** – enter Patient ID, From Staff ID, To Staff ID and click Run Procedure
3. The result or success message will appear below the button

---

## Troubleshooting

**Application does not open**
- Verify Python is installed: `python --version`
- Make sure you are in the correct project folder

**"Database error" message**
- Verify PostgreSQL is running
- Double-check the DB_CONFIG details in `db.py`

**Tkinter not found (Linux only)**
```bash
sudo apt-get install python3-tk
```
