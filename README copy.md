🏥 Medical Staff Management System - Hospital Database

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

6. Future Stages

__________________________________________________________________________________________

**🧾 Overview**

The system is designed to manage the human resource assets of a hospital, specifically focusing on the professional medical team. Key functionalities include:

Shift Scheduling: Managing the many-to-many relationship of staff assignments to shifts.

Role Hierarchy: Organizing data for doctors and nurses while maintaining data integrity.

Department Tracking: Monitoring manpower distribution across various hospital departments.

The system uses foreign keys, specialized roles, and entity relationships to ensure a streamlined workflow for hospital administrators.

_____________________________________________________________________________________________

**🗂️ ERD and DSD Diagrams**

ERD (Entity Relationship Diagram)
<img width="3369" height="2436" alt="image" src="https://github.com/user-attachments/assets/df236ecd-51f7-4b4b-b6db-c26c13cc7c88" />


DSD (Data Structure Diagram)
<img width="2595" height="2427" alt="image" src="https://github.com/user-attachments/assets/8fc35a8e-df50-441f-838d-7986a8c410d4" />

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

**Method A: Python Script**
(Insert screenshot of your Python insertion script here)

**Method B: Mockaroo Generator**
(Insert screenshot of your Mockaroo configuration here)

**Method C: Insert**

_____________________________________________________________________________________________

**💾 Backup & Restore**

Backup Process
(Insert screenshot of your successful pg_dump/Backup here)

Restore Process
(Insert screenshot of your successful Restore here)

-----------------------------------------------------------------------------------------------------
