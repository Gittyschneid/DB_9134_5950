-- ==========================================
-- Integration Phase: Bridge Table Creation
-- ==========================================

-- יצירת הטבלה המקשרת בין הצוות המקומי למטופלים המרוחקים
CREATE TABLE staff_patient_assignment (
    assignment_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL,
    patient_id NUMERIC NOT NULL,
    assignment_date DATE DEFAULT CURRENT_DATE,
    notes VARCHAR(255),
    -- מפתח זר לצוות המקומי
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
    -- הערה למרצה: לא ניתן ליצור מפתח זר (FK) קשיח ל-patient_id 
    -- מכיוון שזו טבלה זרה (Foreign Table) דרך FDW.
);

-- הכנסת נתונים פיקטיביים כדי שיהיה לנו מה לראות במבטים
-- (השותפה תצטרך לוודא שה-IDs האלה קיימים אצלה, או לשנות בהתאם)
INSERT INTO staff_patient_assignment (staff_id, patient_id, notes)
VALUES 
    (15, 1, 'Daily checkup'),
    (15, 2, 'Administering medication'),
    (22, 3, 'Post-surgery evaluation'),
    (40, 4, 'Emergency consultation'),
    (40, 5, 'Discharge review');