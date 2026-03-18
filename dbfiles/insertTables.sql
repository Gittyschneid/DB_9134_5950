-- Departments
INSERT INTO Department VALUES (1, 'Emergency', 'Building A');
INSERT INTO Department VALUES (2, 'Cardiology', 'Building B');

-- Staff
INSERT INTO Staff VALUES (1, 'Dana', 'Levi', 'Doctor', '0501234567', 'dana@example.com', '2022-01-10', 1);

-- Doctor
INSERT INTO Doctor VALUES (1, 'Cardiology', 'LIC123', 1);

-- Shifts
INSERT INTO Shift VALUES (1, 'Morning', '08:00:00', '16:00:00');

-- Staff Shift
INSERT INTO Staff_Shift VALUES (1, '2024-05-01', 1, 1);