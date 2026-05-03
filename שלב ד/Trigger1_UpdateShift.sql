-- 1. Creating the trigger function
CREATE OR REPLACE FUNCTION trg_func_validate_shift_update()
RETURNS TRIGGER AS $$
DECLARE
    v_role VARCHAR(50);
BEGIN
    -- Implicit Cursor: Retrieving the employee role to verify that it exists
    SELECT role INTO STRICT v_role 
    FROM Staff 
    WHERE staff_id = NEW.staff_id;

    -- Branching: Checking if an attempt is made to change a shift date to the past
    IF NEW.shift_date < CURRENT_DATE THEN
        --Throwing an error will stop the UPDATE
        RAISE EXCEPTION 'Invalid Operation: Cannot move shift to a past date (%).', NEW.shift_date;
    END IF;

    -- DML: Recording the change in the audit table (only if the date has actually changed)
    IF OLD.shift_date IS DISTINCT FROM NEW.shift_date THEN
        INSERT INTO Shift_Audit_Log (staff_id, old_shift_date, new_shift_date, changed_by)
        VALUES (NEW.staff_id, OLD.shift_date, NEW.shift_date, CURRENT_USER);
    END IF;

    RETURN NEW; --Confirm the update
    
EXCEPTIoN
    -- Exception Handling: What happens if the employee is deleted or does not exist?
    WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'Security Alert: Staff ID % does not exist in the system.', NEW.staff_id;
END;
$$ LANGUAGE plpgsql;

-- 2. Linking the trigger to the table
CREATE TRIGGER trg_update_shift
BEFORE UPDATE ON Staff_Shift
FOR EACH ROW
EXECUTE FUNCTION trg_func_validate_shift_update();