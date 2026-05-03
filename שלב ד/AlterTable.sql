-- Creating a tracking table to document changes in shifts for medical staff
CREATE TABLE Shift_Audit_Log (
    audit_id SERIAL PRIMARY KEY,
    staff_id INT,
    old_shift_date DATE,
    new_shift_date DATE,
    changed_by VARCHAR(50),
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);