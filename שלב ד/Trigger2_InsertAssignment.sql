-- 1. Creating the Trigger Function
CREATE OR REPLACE FUNCTION trg_func_check_patient_load()
RETURNS TRIGGER AS $$
DECLARE
    v_staff_role VARCHAR(50);
    v_patient_count INT := 0;
    v_max_patients INT;
    v_assignment_rec RECORD; -- Using a Record Variable
    
    -- Explicit cursor
    c_today_assignments CURSOR FOR
        SELECT assignment_id 
        FROM staff_patient_assignment
        WHERE staff_id = NEW.staff_id AND assignment_date = NEW.assignment_date;
BEGIN
    -- Finding the staff role
    SELECT role INTO STRICT v_staff_role FROM Staff WHERE staff_id = NEW.staff_id;

    -- Branching: Determining Maximum Load by Role
    IF v_staff_role = 'Doctor' THEN
        v_max_patients := 5;
    ELSIF v_staff_role = 'Nurse' THEN
        v_max_patients := 8;
    ELSE
        v_max_patients := 3; -- For Managers and Other Staff
    END IF;

    -- A Loop That Runs on the Explicit Cursor to Count Patients
    OPEN c_today_assignments;
    LOOP
        FETCH c_today_assignments INTO v_assignment_rec;
        EXIT WHEN NOT FOUND;
        v_patient_count := v_patient_count + 1;
    END LOOP;
    CLOSE c_today_assignments;

    -- Throwing an Exception if the Worker is Too Busy
    IF v_patient_count >= v_max_patients THEN
        RAISE EXCEPTION 'Workload Limit Exceeded! Staff % (%) cannot take more than % patients on %.', 
            NEW.staff_id, v_staff_role, v_max_patients, NEW.assignment_date;
    END IF;

    RETURN NEW; -- Approval to perform the insertion into the table

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'Assignment failed: Invalid Staff ID provided.';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'An unexpected database error occurred: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- 2. Linking the trigger to the linking table

CREATE TRIGGER trg_insert_assignment
BEFORE INSERT ON staff_patient_assignment
FOR EACH ROW
EXECUTE FUNCTION trg_func_check_patient_load();