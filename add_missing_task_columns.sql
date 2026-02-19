-- Add missing columns to tasks table for advanced features
-- This migration adds the new fields without dropping any existing data

-- Add priority column (default value 'Medium')
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'Medium';

-- Add due_date column (optional datetime field)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;

-- Add reminder_time column (optional datetime field)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP WITH TIME ZONE;

-- Add recurrence_type column (optional, max 20 chars)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS recurrence_type VARCHAR(20);

-- Add recurrence_metadata column (optional, max 500 chars)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS recurrence_metadata VARCHAR(500);

-- Update existing records to set default priority if they have NULL values
UPDATE tasks
SET priority = 'Medium'
WHERE priority IS NULL;

-- Optionally, you can add constraints after adding the columns
-- Add check constraint for priority field (if desired)
-- ALTER TABLE tasks
-- ADD CONSTRAINT check_priority_values CHECK (priority IN ('Low', 'Medium', 'High', 'Critical'));