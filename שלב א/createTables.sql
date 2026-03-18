
-- 1. Department Table
CREATE TABLE Department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL,
    location VARCHAR2(100) NOT NULL,
    CONSTRAINT check_dept_name CHECK (length(department_name) > 0)
);

-- 2. Staff Table
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    role VARCHAR2(30) NOT NULL,
    phone VARCHAR2(20),
    email VARCHAR2(100) UNIQUE,
    hire_date DATE NOT NULL,
    department_id INT NOT NULL,
    CONSTRAINT check_staff_role CHECK (role IN ('Doctor', 'Nurse', 'Admin')),
    CONSTRAINT check_email_format CHECK (email LIKE '%@%.%'),
    CONSTRAINT fk_staff_dept FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- 3. Doctor Table
CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY,
    specialization VARCHAR2(100) NOT NULL,
    license_number VARCHAR2(50) UNIQUE NOT NULL,
    staff_id INT UNIQUE NOT NULL,
    CONSTRAINT fk_doctor_staff FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- 4. Nurse Table
CREATE TABLE Nurse (
    nurse_id INT PRIMARY KEY,
    certification VARCHAR2(100),
    staff_id INT UNIQUE NOT NULL,
    CONSTRAINT fk_nurse_staff FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- 5. Add Head Doctor to Department (1:1)
ALTER TABLE Department ADD COLUMN head_doctor_id INT UNIQUE;
ALTER TABLE Department ADD CONSTRAINT fk_dept_head FOREIGN KEY (head_doctor_id) REFERENCES Doctor(doctor_id);

-- 6. Shift Table
CREATE TABLE Shift (
    shift_id INT PRIMARY KEY,
    shift_name VARCHAR2(50) NOT NULL,
    start_time TIME NOT NULL, -- PostgreSQL uses TIME for hours/minutes
    end_time TIME NOT NULL
);

-- 7. Staff_Shift Table
CREATE TABLE Staff_Shift (
    staff_shift_id INT PRIMARY KEY,
    shift_date DATE NOT NULL,
    staff_id INT NOT NULL,
    shift_id INT NOT NULL,
    CONSTRAINT check_shift_date CHECK (shift_date >= '2020-01-01'),
    CONSTRAINT fk_ss_staff FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    CONSTRAINT fk_ss_shift FOREIGN KEY (shift_id) REFERENCES Shift(shift_id)
);
