********************************************************************************************************
THE 8 SELECT QUERIES:
********************************************************************************************************

1. Monthly Workload Report

SELECT 
    S.first_name, 
    S.last_name, 
    EXTRACT(MONTH FROM SS.shift_date) AS shift_month,
    EXTRACT(YEAR FROM SS.shift_date) AS shift_year,
    COUNT(SS.staff_shift_id) AS total_shifts
FROM Staff S
JOIN Staff_Shift SS ON S.staff_id = SS.staff_id
GROUP BY S.first_name, S.last_name, shift_month, shift_year
HAVING COUNT(SS.staff_shift_id) > 5
ORDER BY shift_year DESC, shift_month DESC;

********************************************************************************************************

2. Department Staffing Levels
  
SELECT D.department_name, D.location, nurse_counts.total
FROM Department D
JOIN (
    SELECT department_id, COUNT(*) AS total
    FROM Staff
    WHERE role = 'Nurse'
    GROUP BY department_id
) nurse_counts ON D.department_id = nurse_counts.department_id
WHERE nurse_counts.total < 30;


********************************************************************************************************

3. Department Head Oversight Report

SELECT 
  D.department_name, 
  S_Head.first_name || ' ' || S_Head.last_name AS head_doctor_name,
  (SELECT COUNT(*) FROM Staff S_Count WHERE S_Count.department_id = D.department_id) AS total_staff_count
FROM Department D
JOIN Doctor Doc ON D.head_doctor_id = Doc.doctor_id
JOIN Staff S_Head ON Doc.staff_id = S_Head.staff_id;

********************************************************************************************************

4. Staff Performance: Low-Volume Responders

SELECT S.first_name, S.last_name, S.role, Q1_data.shift_count
FROM Staff S
JOIN (
    SELECT staff_id, COUNT(*) AS shift_count
    FROM Staff_Shift
    WHERE EXTRACT(MONTH FROM shift_date) BETWEEN 1 AND 3
    GROUP BY staff_id
    HAVING COUNT(*) < 5
) Q1_data ON S.staff_id = Q1_data.staff_id
ORDER BY Q1_data.shift_count DESC;

********************************************************************************************************

5. Active Doctors in Cardiology

SELECT first_name, last_name FROM Staff       //SUBQUERY
WHERE staff_id IN (SELECT staff_id FROM Doctor WHERE specialization = 'Cardiology');

SELECT S.first_name, S.last_name       //JOIN
FROM Staff S 
JOIN Doctor D ON S.staff_id = D.staff_id 
WHERE D.specialization = 'Cardiology';

********************************************************************************************************

6. Identifying "Multi-Role" Staff

SELECT staff_id FROM Doctor     //INTERSECT
INTERSECT
SELECT staff_id FROM Nurse;

SELECT D.staff_id FROM Doctor D        //JOIN
JOIN Nurse N ON D.staff_id = N.staff_id;

********************************************************************************************************

7. Staff with Assignments on a Specific Date

SELECT email FROM Staff S     //EXISTS
WHERE EXISTS (SELECT 1 FROM Staff_Shift SS WHERE SS.staff_id = S.staff_id AND SS.shift_date = '2026-03-20');

SELECT DISTINCT S.email FROM Staff S       //JOIN
JOIN Staff_Shift SS ON S.staff_id = SS.staff_id 
WHERE SS.shift_date = '2026-03-20';

********************************************************************************************************

8. Specialization Availability by Department 

SELECT first_name, last_name, email      //IN SUBQUERY
FROM Staff 
WHERE department_id = 10 
AND staff_id IN (
    SELECT staff_id 
    FROM Doctor 
    WHERE specialization = 'Pediatrics'
);

SELECT S.first_name, S.last_name, S.email       //JOIN
FROM Staff S
JOIN Doctor D ON S.staff_id = D.staff_id
WHERE S.department_id = 10 
AND D.specialization = 'Pediatrics';


********************************************************************************************************
THE 3 UPDATE QUERIES:
********************************************************************************************************
1. Update Department Head for Engineering

-- BEFORE
SELECT * FROM Department
WHERE department_name = 'Engineering';

SELECT * FROM Doctor
WHERE specialization = 'Cardiology';

-- EXECUTE
WITH available_doctors AS (
    SELECT doc.doctor_id
    FROM Doctor doc
    WHERE doc.specialization = 'Cardiology'
      AND doc.doctor_id NOT IN (
          SELECT head_doctor_id
          FROM Department
          WHERE head_doctor_id IS NOT NULL
      )
    ORDER BY doc.doctor_id
    LIMIT 1
)
UPDATE Department d
SET head_doctor_id = ad.doctor_id
FROM available_doctors ad
WHERE d.department_id = (
    SELECT MIN(department_id)
    FROM Department
    WHERE department_name = 'Engineering'
);

-- AFTER
SELECT * FROM Department
WHERE department_name = 'Engineering';
********************************************************************************************************

2. Update Future Shifts from Evening to Night

-- BEFORE
SELECT * FROM Staff_Shift
WHERE shift_id = 2 AND shift_date > CURRENT_DATE
ORDER BY shift_date;

-- EXECUTE
UPDATE Staff_Shift
SET shift_id = 3
WHERE shift_id = 2 AND shift_date > CURRENT_DATE;

-- AFTER
SELECT * FROM Staff_Shift
WHERE shift_date > CURRENT_DATE
ORDER BY shift_date;
********************************************************************************************************

3. Reduce Workload for Overloaded Staff

-- BEFORE
SELECT staff_id, COUNT(*) as future_shifts
FROM Staff_Shift
WHERE shift_date > CURRENT_DATE
GROUP BY staff_id
HAVING COUNT(*) > 3;

-- EXECUTE
UPDATE Staff_Shift
SET shift_id = 1
WHERE staff_id IN (
    SELECT staff_id
    FROM Staff_Shift
    WHERE shift_date > CURRENT_DATE
    GROUP BY staff_id
    HAVING COUNT(*) > 3
)
AND shift_date > CURRENT_DATE;

-- AFTER
SELECT * FROM Staff_Shift
WHERE shift_date > CURRENT_DATE
ORDER BY staff_id, shift_date;

********************************************************************************************************
THE 3 DELETE QUERIES:
********************************************************************************************************
1. Delete Old Shifts

-- BEFORE
SELECT * FROM Staff_Shift
WHERE shift_date < CURRENT_DATE - INTERVAL '1 year';

-- EXECUTE
DELETE FROM Staff_Shift
WHERE shift_date < CURRENT_DATE - INTERVAL '1 year';

-- AFTER
SELECT * FROM Staff_Shift
WHERE shift_date < CURRENT_DATE - INTERVAL '1 year';
********************************************************************************************************

2. Delete Duplicate Shifts

-- BEFORE
SELECT staff_id, shift_id, shift_date, COUNT(*)
FROM Staff_Shift
GROUP BY staff_id, shift_id, shift_date
HAVING COUNT(*) > 1;

-- EXECUTE
DELETE FROM Staff_Shift
WHERE staff_shift_id NOT IN (
    SELECT MIN(staff_shift_id)
    FROM Staff_Shift
    GROUP BY staff_id, shift_id, shift_date
);

-- AFTER
SELECT staff_id, shift_id, shift_date, COUNT(*)
FROM Staff_Shift
GROUP BY staff_id, shift_id, shift_date
HAVING COUNT(*) > 1;
********************************************************************************************************

3. Delete Inactive Departments

-- BEFORE
SELECT * FROM Department d
WHERE NOT EXISTS (
    SELECT 1 FROM Staff s
    WHERE s.department_id = d.department_id
);

-- EXECUTE
DELETE FROM Department d
WHERE NOT EXISTS (
    SELECT 1
    FROM Staff s
    WHERE s.department_id = d.department_id
)
AND NOT EXISTS (
    SELECT 1
    FROM Staff s
    JOIN Staff_Shift ss ON s.staff_id = ss.staff_id
    WHERE s.department_id = d.department_id
    AND ss.shift_date > CURRENT_DATE - INTERVAL '6 months'
);

-- AFTER
SELECT * FROM Department d
WHERE NOT EXISTS (
    SELECT 1 FROM Staff s
    WHERE s.department_id = d.department_id
);