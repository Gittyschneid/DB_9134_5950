-- ==========================================
-- VIEW 1: Our Wing (Medical Staff)
-- Description: Shows the upcoming shifts for all staff members.
-- ==========================================
CREATE OR REPLACE VIEW view_staff_schedule AS
SELECT 
    s.staff_id, 
    s.first_name, 
    s.last_name, 
    s.role, 
    sh.shift_name, 
    ss.shift_date
FROM Staff s
JOIN Staff_Shift ss ON s.staff_id = ss.staff_id
JOIN Shift sh ON ss.shift_id = sh.shift_id;

-- Query 1.1: Get upcoming shifts for Doctors only
SELECT * FROM view_staff_schedule 
WHERE role = 'Doctor' AND shift_date >= CURRENT_DATE 
ORDER BY shift_date 
LIMIT 10;-- ======================================================================
-- VIEW 1: Local Wing (Staff Schedule)
-- Description: Queries purely local tables to view staff shift assignments.
-- ======================================================================
CREATE OR REPLACE VIEW view_staff_schedule AS
SELECT s.staff_id, s.first_name, s.last_name, s.role, sh.shift_name, ss.shift_date
FROM Staff s
JOIN Staff_Shift ss ON s.staff_id = ss.staff_id
JOIN Shift sh ON ss.shift_id = sh.shift_id;

-- Query 1.1: Retrieve the next upcoming shifts for Doctors (Efficiency: LIMIT 10)
SELECT * FROM view_staff_schedule WHERE role = 'Doctor' LIMIT 10;

-- Query 1.2: Analytical query - Total shifts scheduled per staff role
SELECT role, COUNT(*) as shift_count FROM view_staff_schedule GROUP BY role;


-- ======================================================================
-- VIEW 2: Partner Wing (Remote Patient Admissions)
-- Description: Queries purely foreign tables via FDW to view remote data.
-- ======================================================================
CREATE OR REPLACE VIEW view_patient_admissions AS
SELECT p.patient_id, p.first_name, p.last_name, a.admission_type
FROM partner_schema.patient p
JOIN partner_schema.admission a ON p.patient_id = a.patient_id;

-- Query 2.1: Retrieve a sample list of patients and their admission type
SELECT * FROM view_patient_admissions LIMIT 10;

-- Query 2.2: Analytical query - Count of patients per admission type
SELECT admission_type, COUNT(*) as patient_count FROM view_patient_admissions GROUP BY admission_type;


-- ======================================================================
-- VIEW 3: Cross-Database Integration
-- Description: Connects local Staff with remote Patients using the bridge table.
-- ======================================================================
CREATE OR REPLACE VIEW view_integrated_care AS
SELECT 
    s.first_name AS staff_name, s.role,
    p.first_name AS patient_name, p.last_name AS patient_surname,
    spa.assignment_date, a.admission_type
FROM Staff s
JOIN staff_patient_assignment spa ON s.staff_id = spa.staff_id
JOIN partner_schema.patient p ON spa.patient_id = p.patient_id
LEFT JOIN partner_schema.admission a ON p.patient_id = a.patient_id;

-- Query 3.1: Retrieve the most recent integrated treatments
SELECT * FROM view_integrated_care ORDER BY assignment_date DESC LIMIT 10;

-- Query 3.2: Analytical query - Total patient interactions per staff role
SELECT role, COUNT(*) as treatments_given FROM view_integrated_care GROUP BY role;

-- Query 1.2: Count how many shifts each role has in the system
SELECT role, COUNT(*) as total_shifts 
FROM view_staff_schedule 
GROUP BY role;


-- ==========================================
-- VIEW 2: Partner Wing (Patient Admissions)
-- Description: Shows patients and their current admission types using remote tables.
-- ==========================================
CREATE OR REPLACE VIEW view_patient_admissions AS
SELECT 
    p.patient_id, 
    p.first_name AS patient_first_name, 
    p.last_name AS patient_last_name, 
    a.admission_type
FROM patient_remote p
JOIN admission_remote a ON p.patient_id = a.patient_id;

-- Query 2.1: Find all patients with an 'Emergency' admission
SELECT * FROM view_patient_admissions 
WHERE admission_type = 'Emergency' 
LIMIT 10;

-- Query 2.2: Count how many patients are in each admission type
SELECT admission_type, COUNT(*) as patient_count 
FROM view_patient_admissions 
GROUP BY admission_type;


-- ==========================================
-- VIEW 3: Integrated View (Staff & Patients)
-- Description: The ultimate integration view! Shows which staff member is treating which remote patient.
-- ==========================================
CREATE OR REPLACE VIEW view_integrated_care AS
SELECT 
    s.first_name AS staff_first_name, 
    s.last_name AS staff_last_name, 
    s.role,
    p.first_name AS patient_first_name, 
    p.last_name AS patient_last_name, 
    spa.assignment_date, 
    a.admission_type
FROM Staff s
JOIN staff_patient_assignment spa ON s.staff_id = spa.staff_id
JOIN patient_remote p ON spa.patient_id = p.patient_id
LEFT JOIN admission_remote a ON p.patient_id = a.patient_id;

-- Query 3.1: See the integrated roster (who is treating whom today)
SELECT * FROM view_integrated_care 
ORDER BY assignment_date DESC 
LIMIT 10;

-- Query 3.2: Find all patients being treated specifically by Nurses
SELECT patient_first_name, patient_last_name, admission_type 
FROM view_integrated_care 
WHERE role = 'Nurse' 
LIMIT 10;