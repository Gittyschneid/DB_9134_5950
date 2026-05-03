**🏥 Medical Staff Management System - Hospital Database**

**📘 Project Report**
This project is a comprehensive Medical Staff Management System designed to manage the human resources of a hospital, focusing on doctors, nurses, and shift scheduling. It was developed as part of a database course project.

**🧑‍💻 Authors**

*Gitty Schneider (333805950)

*Avital Tal (214939134)

**🏢 Project Scope**

*System: Hospital Management System

*Unit: Medical Staff Management

_______________________________________________________________________________________

**📌 Table of Contents**

1. Overview

2. ERD and DSD Diagrams

3. Data Structure Description

4. Data Insertion Methods

5. Backup & Restore

6. Stage 2 – Advanced SQL Queries & Constraints

    *SELECT Queries
   
    *DELETE Queries
   
    *UPDATE Queries
   
    *Rollback & Commit Transactions
   
    *Constraints Using ALTER TABLE
   
6. Stage 3 – Advanced SQL Queries & Constraints

    *DSD new
   
    *ERD new 

    *Integrated/ combined DSD
   
    *Integrated/ combined ERD
   
    *Integration decisions made
   
    *Explanation of the processes and the commands

7. Stage 4 – Advanced PL/pgSQL Programs
   
    *Functions
   
    *Procedures
   
    *Triggers
   
    *Main Programs



__________________________________________________________________________________________

**🧾 Stage 1- Overview**

The system is designed to manage the human resource assets of a hospital, specifically focusing on the professional medical team. Key functionalities include:

Shift Scheduling: Managing the many-to-many relationship of staff assignments to shifts.

Role Hierarchy: Organizing data for doctors and nurses while maintaining data integrity.

Department Tracking: Monitoring manpower distribution across various hospital departments.

The system uses foreign keys, specialized roles, and entity relationships to ensure a streamlined workflow for hospital administrators.

Link for the site we made with AI Studio:
file:///Users/gitty/Desktop/SCHOOL/מיניפ%20בסנת/DB_9134_5950/management.html
_____________________________________________________________________________________________

**🗂️ ERD and DSD Diagrams**

ERD (Entity Relationship Diagram)
<img width="3369" height="2436" alt="image" src="https://github.com/user-attachments/assets/df236ecd-51f7-4b4b-b6db-c26c13cc7c88" />


DSD (Data Structure Diagram)
<img width="4080" height="2802" alt="image" src="https://github.com/user-attachments/assets/9c79f69d-0e41-451c-b741-953a2f531561" />

________________________________________________________________________________________________

**🗃️ Data Structure Description**

Below is a summary of the main entities and their fields:

Staff (Base Entity)
Represents all medical personnel.

Staff_ID (Primary Key)

FirstName

LastName

Role (Doctor/Nurse)

Nurses
Nurse_ID (Foreign Key to Staff)

Certification_Level

Department_ID

Shifts
Shift_ID (Primary Key)

Shift_Date

Shift_Type (Morning/Evening/Night)

_____________________________________________________________________________________________

**📥 Data Insertion Methods**

**Method A: Mockaroo Data Generation**

Data was generated using the Mockaroo website.

We defined schemas that match the database tables and generated sample data.

The generated output was exported as SQL files.

These SQL scripts were executed in pgAdmin to insert data into the database.

<img src="Images/Stage_1/Generating department - mockaroo.png" width="600"/>

<img src="Images/Stage_1/Generating department.jpg" width="600"/>

**Method B: CSV Import using pgAdmin**

Some of the generated data was exported as CSV files and imported into PostgreSQL using pgAdmin.

During the import process, several issues were encountered:

- Some tables required matching the exact number of columns.
- One of the CSV imports failed due to missing values in a column that did not allow NULL.
- The issue was resolved by adjusting the data and ensuring compatibility with the table structure.

After fixing the issues, the CSV files were successfully imported into the relevant tables.

<img src="Images/Stage_1/import.jpg" width="600"/>

**Method C: Insert with Python Script**

-- 1. הכנסת 500 מחלקות
INSERT INTO Department (department_id, department_name, location)
SELECT 
    i, 
    'Department ' || i, 
    'Building ' || ((i % 5) + 1) || ', Room ' || i
FROM generate_series(1, 500) AS i;

-- 2. הכנסת 500 עובדים (Staff)
INSERT INTO Staff (staff_id, first_name, last_name, role, phone, email, hire_date, department_id)
SELECT 
    i, 
    'FirstName_' || i, 
    'LastName_' || i, 
    CASE 
        WHEN i <= 200 THEN 'Doctor' 
        WHEN i <= 450 THEN 'Nurse' 
        ELSE 'Admin' 
    END,
    '050-' || LPAD(i::text, 7, '0'),
    'staff' || i || '@hospital.org',
    CURRENT_DATE - (i || ' days')::interval,
    (i % 500) + 1 -- מקשר למחלקות שיצרנו
FROM generate_series(1, 500) AS i;

-- 3. הכנסת רופאים (200 הראשונים מה-Staff הם דוקטורים)
INSERT INTO Doctor (doctor_id, specialization, license_number, staff_id)
SELECT 
    i, 
    CASE WHEN i % 2 = 0 THEN 'Cardiology' ELSE 'Pediatrics' END,
    'LIC-' || i || '-XYZ',
    i
FROM generate_series(1, 200) AS i;

-- 4. הכנסת אחיות (עובדים 201 עד 450)
INSERT INTO Nurse (nurse_id, certification, staff_id)
SELECT 
    i - 200, 
    'Advanced Care Cert ' || i,
    i
FROM generate_series(201, 450) AS i;

-- 5. הכנסת 500 משמרות (Shift)
INSERT INTO Shift (shift_id, shift_name, start_time, end_time)
SELECT 
    i, 
    'Shift ' || i, 
    '08:00:00', 
    '16:00:00'
FROM generate_series(1, 500) AS i;

-- 6. הטבלה הגדולה: 20,000 שיבוצי עובדים (Staff_Shift)
INSERT INTO Staff_Shift (staff_shift_id, shift_date, staff_id, shift_id)
SELECT 
    i, 
    '2024-01-01'::date + (i % 365 || ' days')::interval, -- מפזר על פני שנה
    (i % 500) + 1, -- רץ על 500 העובדים
    (i % 500) + 1  -- רץ על 500 המשמרות
FROM generate_series(1, 20000) AS i;

<img width="923" height="1113" alt="image" src="https://github.com/user-attachments/assets/921dc6fb-f464-46a3-b335-7a9a60a15ba4" />


_____________________________________________________________________________________________

**💾 Backup & Restore**

Backup Process
**Backup Process**

A database backup was created using pgAdmin.

The backup process was initiated from the database interface, and a .backup file was generated.

The backup file is included in the project repository.

Although the backup file appears as a binary file and is not readable as plain text, this is expected behavior for PostgreSQL backup files.

The backup operation demonstrates the ability to export the full database for recovery purposes.

<img src="Images/Stage_1/backup.jpg" width="600"/>
<img width="2805" height="173" alt="image" src="https://github.com/user-attachments/assets/e7be678d-ce88-40ff-939d-8b9d6fef52a6" />


-----------------------------------------------------------------------------------------------------
**📘 Stage 2 – Advanced SQL Queries & Constraints**
-----------------------------------------------------------------------------------------------------

This section includes documentation and screenshots for advanced SQL queries (SELECT, DELETE, UPDATE) and constraint handling as required in Stage 2.

**📊 SELECT Queries**

A total of 8 SELECT queries were implemented. Each query is described and accompanied by screenshots.

🔍 SELECT 1: Monthly Workload Report 

This is for the "Management Dashboard" screen to see how many shifts each staff member did per month.

<img width="647" height="496" alt="Screenshot 2026-04-15 at 14 28 00" src="https://github.com/user-attachments/assets/66721e1d-9f81-403d-b065-af5ce3d53678" />

🔍 SELECT 2: Department Staffing Levels

Find departments that have fewer than 30 Nurses assigned

<img width="543" height="490" alt="Screenshot 2026-04-15 at 14 28 30" src="https://github.com/user-attachments/assets/cec8f9ab-f3ad-4835-af2d-bdffb745a3b1" />

🔍 SELECT 3: Staff Performance: Low-Volume Responders

Finds staff members who have worked less than 5 shifts in the first quarter of the year.

<img width="581" height="692" alt="Screenshot 2026-04-15 at 14 30 09" src="https://github.com/user-attachments/assets/8d788ed7-f109-42f7-af98-aa4ebed00f52" />

🔍 SELECT 4: Department Head Oversight Report

Joins 3 tables to show Department names, their Head Doctors, and the total staff in that department.

<img width="643" height="616" alt="Screenshot 2026-04-15 at 14 29 04" src="https://github.com/user-attachments/assets/c00be5db-5eb5-4f9a-bb47-0955ebe0a18a" />

(The 4 Double Queries- Efficiency Comparison)

🔍 SELECT 5: Active Doctors in Cardiology

Option A (Subquery) Option B (JOIN):

<img width="885" height="731" alt="Screenshot 2026-03-28 at 21 09 05" src="https://github.com/user-attachments/assets/fc514a48-8f0c-4ebe-8ca1-d1ccfe846e6d" />

<img width="882" height="733" alt="Screenshot 2026-03-28 at 21 08 01" src="https://github.com/user-attachments/assets/61f46d8c-1e8e-490a-8142-5b19c418b9ce" />

🔍 SELECT 6:Identifying "Multi-Role" Staff

Find staff members who are registered as both a Doctor and a Nurse (Data Integrity check).

Option A (INTERSECT) Option B (JOIN):

<img width="888" height="433" alt="Screenshot 2026-03-28 at 21 11 22" src="https://github.com/user-attachments/assets/b79e316d-4bde-461c-a5c2-b0e319a7da29" />

<img width="883" height="436" alt="Screenshot 2026-03-28 at 21 11 36" src="https://github.com/user-attachments/assets/b968823d-9e74-4ad5-9b6b-394ae0d8987f" />

🔍 SELECT 7: Staff with Assignments on a Specific Date

Find the emails of staff members working on '2026-03-20'

Option A (EXISTS) Option B (JOIN):

<img width="1000" height="572" alt="Screenshot 2026-03-28 at 21 14 08" src="https://github.com/user-attachments/assets/03f320ea-53d4-4c2b-94cd-fb44d39cea1d" />

<img width="1001" height="576" alt="Screenshot 2026-03-28 at 21 14 26" src="https://github.com/user-attachments/assets/253bab24-9372-444c-ae02-9f1cc25341be" />

🔍 SELECT 8: Specialization Availability by Department

ist the names and emails of all Doctors who are specialized in 'Pediatrics' and work in Department ID 1

Option A (IN Subquery) Option B (JOIN):

<img width="1007" height="575" alt="Screenshot 2026-03-28 at 21 22 51" src="https://github.com/user-attachments/assets/6199cc22-1463-44f7-8c7d-4f0e298ce8a9" />

<img width="1001" height="580" alt="Screenshot 2026-03-28 at 21 23 13" src="https://github.com/user-attachments/assets/70667b32-5a10-4f58-9963-514faf64c183" />

-----------------------------------------------------------------------------------------------------

**📊 DELETE Queries**
🔍 DELETE 1: Removing Old Shift Records

To maintain database efficiency and reduce unnecessary data storage, old shift records that are no longer relevant were removed from the system.

This query:
Deletes shifts older than one year
Keeps only relevant and recent data
SQL Features Used
Date comparison
INTERVAL usage

<img src="Images/stage_2/DELETE 1-before.jpg" width="600"/>

<img src="Images/stage_2/DELETE 1-after.jpg" width="600"/>

🔍 DELETE 2: Removing Duplicate Shift Records

During data entry or imports, duplicate shift records may occur.
This query ensures data integrity by removing duplicate records while keeping one valid entry.

This query:
Identifies duplicate rows based on:
staff_id
shift_id
shift_date
Keeps only the earliest record using MIN
Deletes all other duplicates
SQL Features Used
Subquery
GROUP BY
Aggregate function (MIN)

<img src="Images/stage_2/DELETE 2-before.jpg" width="600"/>

<img src="Images/stage_2/EDLETE 2-after.jpg" width="600"/>

🔍 DELETE 3: Removing Inactive Departments

Over time, some hospital departments may become inactive and no longer have staff assigned to them.
To keep the system clean and accurate, these unused departments were removed.

This query:
Deletes departments that:
Have no staff assigned
Have no recent activity
Uses a safe approach to avoid foreign key violations
SQL Features Used
NOT EXISTS
JOIN
Date filtering with INTERVAL

<img src="Images/stage_2/DELETE 3-before.jpg" width="600"/>

<img src="Images/stage_2/DELETE 3-after.jpg" width="600"/>

-----------------------------------------------------------------------------------------------------

**📊 UPDATE Queries**
🔍 UPDATE 1: Assigning a New Head Doctor to the Engineering Department

In the hospital system, an Engineering department required a new head doctor due to administrative changes.
To simulate a realistic management decision, we selected a doctor with the specialization Cardiology and assigned them as the new head of the department.

This query:
Selects a doctor with a specific specialization (Cardiology)
Assigns that doctor as the head of the Engineering department
SQL Features Used
Subquery
LIMIT (to ensure only one doctor is selected)

<img src="Images/stage_2/UPDATE 1-before.jpg" width="600"/>

<img src="Images/stage_2/UPDATE 1-after.jpg" width="600"/>

🔍 UPDATE 2: Modifying Future Shifts

Due to increased workload and operational needs, hospital management decided to adjust future shift assignments.
All upcoming Evening shifts (Shift 2) were reassigned to Night shifts (Shift 3) to ensure better coverage.

This query:
Targets only future shifts
Updates shift type from 2 → 3
Leaves past data unchanged
SQL Features Used
Date filtering using CURRENT_DATE

<img src="Images/stage_2/UPDATE 2-before.jpg" width="600"/>

<img src="Images/stage_2/UPDATE 2-after.jpg" width="600"/>

🔍 UPDATE 3: Balancing Workload for Overloaded Staff

The hospital system identified staff members who were assigned to multiple shifts, potentially causing workload imbalance.
To prevent staff burnout and improve scheduling fairness, their future shifts were reassigned to a lighter shift type.

This query:
Identifies staff with more than 3 shifts using GROUP BY and HAVING
Updates only their future shifts
Reassigns them to Shift 1 (lighter workload)
SQL Features Used
Subquery
GROUP BY + HAVING
Date filtering

<img src="Images/stage_2/UPDATE 3-before.jpg" width="600"/>

<img src="Images/stage_2/UPDATE 3-after.jpg" width="600"/>

-----------------------------------------------------------------------------------------------------

**Rollback & Commit Transactions**

Rollback Demonstration

We simulated a mass email update error and used ROLLBACK to restore data integrity.

 Database state during the transaction (Unsaved Error):
 
<img width="1223" height="759" alt="Screenshot 2026-03-28 at 22 22 35" src="https://github.com/user-attachments/assets/4c8f1de2-0bb2-483d-ae85-73736eb18043" />

 Database state after ROLLBACK (Data Restored):

<img width="1225" height="759" alt="Screenshot 2026-03-28 at 22 23 15" src="https://github.com/user-attachments/assets/7dc96a66-4fd7-49f5-a865-1552a345e883" />

Commit Demonstration

We successfully updated the hospital wing location and used COMMIT to save the changes permanently.

Previewing the location update:

<img width="1229" height="514" alt="Screenshot 2026-03-28 at 22 23 52" src="https://github.com/user-attachments/assets/114e1599-d139-46a0-9fb2-11dbd3236770" />

Final state after COMMIT:

<img width="1232" height="508" alt="Screenshot 2026-03-28 at 22 24 28" src="https://github.com/user-attachments/assets/35fe13d0-cfb0-41e9-96b4-a1012ead1036" />


-----------------------------------------------------------------------------------------------------

**Constraints Using ALTER TABLE**

<img width="885" height="733" alt="Screenshot 2026-03-28 at 20 53 28" src="https://github.com/user-attachments/assets/8768da5f-9478-4847-b2d2-ec49ff3e76a1" />


-----------------------------------------------------------------------------------------------------
**📘 Stage 3 – Integration and Views**
-----------------------------------------------------------------------------------------------------

📜This stage focuses on integrating the Financial Department database with the Dormitory Management database — a crucial component of the overall university management system. The objective is to build a unified structure that enables a comprehensive view of student-related information, combining both financial and residential data. As part of this integration, SQL views were created from both the perspective of our department and the collaborating department. These views provide streamlined, role-specific access to the combined data, making it easier for each side to retrieve and analyze the information most relevant to their operational needs.

-----------------------------------------------------------------------------------------------------

**🗂️ DSD new**

<img width="5280" height="2802" alt="DSD diagram" src="https://github.com/user-attachments/assets/234cf1bb-7b9a-42cb-903f-ab2f9fe23a58" />

-----------------------------------------------------------------------------------------------------

**🗂️ ERD new**

<img width="5280" height="2802" alt="ERD diagram" src="https://github.com/user-attachments/assets/4a08b166-36a5-4af4-ac9f-4a98f9a71c3e" />

-----------------------------------------------------------------------------------------------------

**🗂️ Integrated/ combined DSD**

<img width="1582" height="816" alt="WhatsApp Image 2026-04-18 at 23 27 39" src="https://github.com/user-attachments/assets/46bd3525-606b-487e-bddd-115cbc6bd923" />

-----------------------------------------------------------------------------------------------------

**🗂️ Integrated/ combined ERD**

<img width="1600" height="1496" alt="WhatsApp Image 2026-04-18 at 23 15 37" src="https://github.com/user-attachments/assets/271187fc-219a-4b6d-b5b7-896ab17f7f38" />


-----------------------------------------------------------------------------------------------------

**🏗️ Integration decisions made**

1. The Core Strategy: Option B (Foreign Tables)

We chose to implement the integration using Option B, which utilizes Foreign Data Wrappers (FDW).

The Decision: Instead of migrating all data into a single schema (Option C), we kept the two databases independent.

The Logic: This mimics a real-world hospital scenario where different departments (Staff HR vs. Clinical Patient Care) might use different software systems but need to share specific data for daily operations. It ensures data remains "owned" by the original department.

2. The Integration Point (The Bridge)

The Decision: We identified the Staff table (our system) and the Patient table (the external system) as the primary points of connection.

The Logic: A Many-to-Many (M:N) relationship was established. In a clinical setting, one doctor or nurse treats many patients, and one patient can be treated by multiple staff members (specialists, residents, etc.).

The Process: We created a local bridge table, staff_patient_assignment, which stores the IDs from both systems to link them without altering the original table structures.

-----------------------------------------------------------------------------------------------------

**💻 Explanation of the processes and the commands**


The integration was performed in three technical phases:

Phase 1: Establishing the Connection

We used the postgres_fdw extension to create a bridge between the local "Medical Staff" database and the remote "Patient" database.

CREATE EXTENSION postgres_fdw: Installs the library that allows PostgreSQL to talk to other PostgreSQL servers.

CREATE SERVER: Defines the location and name of the partner's database.

CREATE USER MAPPING: Provides the credentials needed to securely access the partner's data.

Phase 2: Virtualizing the External Data

We created Foreign Tables to act as "windows" into the other group's database.

CREATE FOREIGN TABLE: This command does not copy data; it creates a local definition of the remote table. This allowed us to query patient_remote as if it were a local table, even though the data lives elsewhere.

Phase 3: Creating Meaningful Views

To prove the integration was successful, we wrote complex Views that perform JOIN operations across the local and foreign tables.

The Process: We used a 4-way JOIN connecting Staff → staff_patient_assignment → patient_remote → admission_remote.

The Result: This provides a unified "Doctor-Patient Roster" that shows real-time hospital activity, fulfilling the project requirements for non-trivial queries.

### 📊 Views & Queries Implementation

To prove the success of our integration and ensure high performance, we designed three distinct views.

#### 🔹 VIEW 1: Local Wing (Staff Schedule)
**Description:** This view queries our local `Medical Staff` database to show the upcoming shifts for all staff members, combining data from the `Staff`, `Staff_Shift`, and `Shift` tables.
**Executed Queries:**
1. Retrieve the next upcoming shifts specifically for Doctors.
2. Analytical query showing the total number of shifts scheduled per staff role.

<img src="Images/stage_3/view-1.jpg" width="600"/>

-----------------------------------------------------------------------------------------------------

#### 🔹 VIEW 2: Partner Wing (Remote Patient Admissions)
**Description:** This view successfully queries the remote `Patient` database (using our `partner_schema` FDW) to display patients and their current admission types, proving connectivity without physical data migration.
**Executed Queries:**
1. Retrieve a sample list of patients and their current admission types from the foreign tables.
2. Analytical query analyzing the remote data to count the number of patients per admission type.

<img src="Images/stage_3/view-2.jpg" width="600"/>

-----------------------------------------------------------------------------------------------------

#### 🔹 VIEW 3: Cross-Database Integration (The Bridge)
**Description:** The core of our Option B integration. It joins the local `Staff` table with the remote `Patient` and `Admission` tables using our `staff_patient_assignment` bridge table, providing a real-time "Doctor-Patient Roster".
**Executed Queries:**
1. The Integrated Roster: Shows exactly which local staff member is currently treating which remote patient.
2. Workload Analysis: An analytical query showing how many patient interactions each staff role has handled across the integrated system.

<img src="Images/stage_3/view-3.jpg" width="600"/>

-----------------------------------------------------------------------------------------------------
**Stage 4 – Advanced PL/pgSQL Programs**
-----------------------------------------------------------------------------------------------------

**Functions**

**Function 1**

This function serves as a strategic management tool for decision-making within the medical wing. It enables department heads to identify the "under-utilization" of human resources by calculating the number of staff members who have completed a low volume of shifts—specifically those at or below a defined threshold (in this case, one shift or fewer).

<img width="978" height="906" alt="Screenshot 2026-05-03 at 12 27 47" src="https://github.com/user-attachments/assets/0970d1a4-f715-44fa-aec4-62a8f37b0f10" />

Proof of running:

<img width="616" height="234" alt="Screenshot 2026-05-03 at 12 34 40" src="https://github.com/user-attachments/assets/38016f87-2d1e-4c2f-8d69-88af6561c0ac" />

**Function 2**

This function acts as a clinical reporting tool that generates a dynamic roster of patients assigned to a specific medical staff member. It is specifically designed to work with the Integrated Wing (Step C), bridging the local Staff database with the remote Patient database using the Staff_Patient_Assignment table.

<img width="877" height="901" alt="FUNCTION_2" src="https://github.com/user-attachments/assets/53e81c32-43b9-4e36-ac20-679fa83380cc" />

Proof of running:

<img width="606" height="612" alt="F2_PROOF" src="https://github.com/user-attachments/assets/34e80f6b-b356-49d7-80c3-92df080474ee" />

-----------------------------------------------------------------------------------------------------

**Procedures**

**Procedure 1**

This procedure handles moving a patient from one doctor/staff member to another.

<img width="963" height="928" alt="PROCEDURE_1" src="https://github.com/user-attachments/assets/17d19177-bf12-42c8-93a5-53d58412c389" />

Proof of running:

<img width="665" height="287" alt="P1_PROOF" src="https://github.com/user-attachments/assets/90c24e81-45b4-4087-9f41-2445130337e5" />

**Procedure 2**

This procedure is highly professional because it uses Transfers to prevent burnout. It moves a specific number of patients from a busy staff member to a less busy one.

<img width="922" height="906" alt="PROCEDURE_2" src="https://github.com/user-attachments/assets/c03043e5-febb-4438-bbb6-c86dd813a1f9" />

Proof of running:

<img width="686" height="286" alt="P2_PROOF1" src="https://github.com/user-attachments/assets/e614b0ef-b4e6-4f25-b464-fb72b339ea49" />
<img width="632" height="305" alt="P2_PROOF2" src="https://github.com/user-attachments/assets/03e2b19c-e318-4229-a082-8d34bfc85fd2" />


-----------------------------------------------------------------------------------------------------
---
### Triggers

**Trigger 1: Data Integrity & Audit Guard**
This trigger functions as an automated compliance and auditing mechanism for staff scheduling. It operates on the `Staff_Shift` table to prevent administrative errors, actively blocking any attempts to reschedule shifts to past dates (preserving historical accuracy). Furthermore, it implements a DML tracking system that automatically logs all valid schedule modifications into a dedicated `Shift_Audit_Log` table, ensuring complete traceability of administrative actions.

**Proof of running:**

<img src="Images/stage_4/Exception blocking (shift update).jpg" width="600"/>

<img src="Images/stage_4/trigger-1.jpg" width="600"/>

**Trigger 2: Clinical Workload Management**
Designed specifically for our integrated cross-database system (Step C), this trigger acts as a safety guardrail to prevent medical staff burnout and ensure quality patient care. Before assigning a new remote patient to a local staff member in the `staff_patient_assignment` bridge table, it dynamically calculates the staff member's current daily workload. It enforces strict, role-specific clinical capacities (e.g., maximum 5 patients for Doctors, 8 for Nurses) and automatically blocks any assignments that exceed this safety threshold.

**Proof of running:**

<img src="Images/stage_4/trigger-2.jpg" width="600"/>

---
### Main Programs (Execution Blocks)

To demonstrate the full integration and orchestration of our PL/pgSQL components, we developed two main anonymous execution blocks (DO blocks). These programs are highly dynamic, using `SELECT INTO` statements to find relevant data at runtime rather than relying on hardcoded IDs.

**Main Program 1: Automated Workload Balancing System**
This anonymous block acts as an advanced administrative automation script. It dynamically queries the database to identify the most overloaded staff member across the system, and locates an available staff member within a specific department (e.g., Cardiology). It then integrates `Function 1` to verify under-utilization and calls `Procedure 2` to automatically transfer a batch of patients, effectively balancing the hospital's workload in real-time.
**Proof of running:**

<img src="Images/stage_4/main-1.jpg" width="600"/>

**Main Program 2: Automated Patient Transfer Protocol**
This program automates specific clinical handoffs. It dynamically identifies a staff member currently treating patients and an available target staff member. Using `Function 2`, it retrieves a dynamic roster (RefCursor) of the source staff's patients, fetches the first assigned patient from the cursor, and immediately executes `Procedure 1` to safely transfer that specific patient to the new medical staff member.
**Proof of running:**

<img src="Images/stage_4/main-2.jpg" width="600"/>
