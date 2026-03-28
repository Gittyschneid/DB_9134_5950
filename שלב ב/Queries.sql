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

