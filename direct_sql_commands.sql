-- Direct SQL commands to add missing columns to your tasks table
-- Copy and execute these in your PostgreSQL client (like pgAdmin, DBeaver, or psql)

-- Add priority column (default value 'Medium')
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'Medium';
COMMENT ON COLUMN tasks.priority IS 'Task priority level: Low, Medium, High, Critical';

-- Add due_date column (optional datetime field)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;
COMMENT ON COLUMN tasks.due_date IS 'Optional due date for the task';

-- Add reminder_time column (optional datetime field)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP WITH TIME ZONE;
COMMENT ON COLUMN tasks.reminder_time IS 'Optional reminder time for the task';

-- Add recurrence_type column (optional, max 20 chars)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_type VARCHAR(20);
COMMENT ON COLUMN tasks.recurrence_type IS 'Recurrence pattern: daily, weekly, monthly';

-- Add recurrence_metadata column (optional, max 500 chars)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_metadata VARCHAR(500);
COMMENT ON COLUMN tasks.recurrence_metadata IS 'Additional recurrence data';

-- Update existing records to set default priority if they have NULL values
UPDATE tasks SET priority = 'Medium' WHERE priority IS NULL;

-- Verify the new columns were added
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'tasks'
  AND column_name IN ('priority', 'due_date', 'reminder_time', 'recurrence_type', 'recurrence_metadata');