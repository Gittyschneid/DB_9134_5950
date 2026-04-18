-- ==========================================
-- Phase 1: Integration - Bridge Table Creation
-- Methodology: Option B (Foreign Tables with Soft Key)
-- ==========================================

CREATE TABLE staff_patient_assignment (
    assignment_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL,
    patient_id NUMERIC NOT NULL,
    assignment_date DATE DEFAULT CURRENT_DATE,
    notes VARCHAR(255),
    -- Local Foreign Key enforcing integrity on our Staff table
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
    -- Note for integration: patient_id acts as a 'Soft Key'. 
    -- A hard FOREIGN KEY cannot be enforced across a Foreign Data Wrapper (FDW).
);

-- Seeding initial data for integration views
INSERT INTO staff_patient_assignment (staff_id, patient_id, notes)
VALUES 
    (2, 1, 'Initial consultation in ER'),
    (3, 2, 'Follow-up appointment'),
    (6, 3, 'Treatment planning'),
    (15, 4, 'Routine checkup'),
    (20, 5, 'Discharge paperwork');