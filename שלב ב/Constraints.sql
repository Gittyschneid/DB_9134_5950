During the implementation of Step B, we encountered a constraint violation. 
This demonstrated the importance of data integrity. 
We resolved this by cleaning the existing 'Shift' records before applying the ALTER TABLE command.

-- Constraint 1: Ensure shift end time is strictly after start time
ALTER TABLE Shift 
ADD CONSTRAINT check_shift_duration CHECK (end_time > start_time);

-- Constraint 2: Validate email format using a Pattern Match
ALTER TABLE Staff 
ADD CONSTRAINT check_email_validity CHECK (email LIKE '%@%.%');

-- Constraint 3: Ensure hire_date is not set in the future
ALTER TABLE Staff 
ADD CONSTRAINT check_hire_date_limit CHECK (hire_date <= CURRENT_DATE);
