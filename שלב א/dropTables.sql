
-- 1. Drop tables. Using CASCADE automatically removes related foreign keys.
-- We drop them in reverse order of creation for safety.

DROP TABLE IF EXISTS Staff_Shift CASCADE;
DROP TABLE IF EXISTS Shift CASCADE;
DROP TABLE IF EXISTS Nurse CASCADE;
DROP TABLE IF EXISTS Doctor CASCADE;
DROP TABLE IF EXISTS Staff CASCADE;
DROP TABLE IF EXISTS Department CASCADE;

-- 2. Optional: Clean up any remaining constraints if needed
-- (Though CASCADE usually handles this perfectly in Postgres)
