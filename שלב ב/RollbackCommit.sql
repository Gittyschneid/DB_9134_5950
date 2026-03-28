-- ========================================================================================================
-- 1. DEMONSTRATING ROLLBACK TRANSACTION 
-- Scenario: An administrator accidentally tries to bulk-update all staff emails with a prefix.
-- This shows how we can undo a mass mistake before it becomes permanent.
-- ========================================================================================================

-- Start the transaction
BEGIN;

-- Action: Update all emails to include 'hospital-il-' before the '@' symbol
UPDATE Staff
SET email = SUBSTRING(email, 1, POSITION('@' IN email) - 1) || 'hospital-il-' || SUBSTRING(email, POSITION('@' IN email), LENGTH(email))
WHERE email NOT LIKE '%hospital-il-%';

-- Verification: Check the temporary state. You will see the 'hospital-il-' prefix.
SELECT staff_id, first_name, email 
FROM Staff 
LIMIT 5;

-- Undo the transaction
ROLLBACK;

-- Verification: Check the state after rollback. The emails should be back to their original form.
SELECT staff_id, first_name, email 
FROM Staff 
LIMIT 5;


-- ========================================================================================================
-- 2. DEMONSTRATING COMMIT TRANSACTION 
-- Scenario: Successfully moving a specific department to a new wing in the hospital.
-- This shows how we finalize and save a valid change to the database.
-- ========================================================================================================

-- Start a new transaction
BEGIN;

-- Action: Move 'Department 1' to the new specialized wing
UPDATE Department
SET location = 'South Wing - Floor 4'
WHERE department_id = 1;

-- Preview: See the change BEFORE committing.
SELECT department_id, department_name, location
FROM Department
WHERE department_id = 1;

-- Save the change permanently
COMMIT;

-- Final Confirmation: Prove the data remains updated after the transaction is finalized.
SELECT department_id, department_name, location
FROM Department
WHERE department_id = 1;
