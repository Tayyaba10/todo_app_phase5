"""
Migration script to add missing columns to tasks table
This script can be run directly to update the database schema
"""
import os
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
import time

def add_missing_task_columns():
    """Add missing columns to the tasks table using raw SQL"""

    # Get database URL from environment or .env file
    database_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/your_database_name')

    if 'DATABASE_URL' not in os.environ:
        # Load from .env file
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        database_url = line.split('=', 1)[1].strip()
                        if database_url.startswith('"') and database_url.endswith('"'):
                            database_url = database_url[1:-1]
                        break
        except FileNotFoundError:
            pass

    if not database_url or database_url.startswith('postgresql://user:password'):
        print("DATABASE_URL environment variable not properly set!")
        print(f"Current value: {database_url}")
        return

    print(f"Connecting to database: {database_url}")

    try:
        # Parse the database URL for psycopg2 connection
        parsed = urlparse(database_url)

        # Connect with SSL parameters for Neon
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove the leading '/'
            user=parsed.username,
            password=parsed.password,
            sslmode='require'  # Add SSL mode for Neon
        )

        # SQL statements to add missing columns
        alter_statements = [
            # Add priority column
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'Medium';",
            "COMMENT ON COLUMN tasks.priority IS 'Task priority level: Low, Medium, High, Critical';",

            # Add due_date column (optional datetime field)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;",
            "COMMENT ON COLUMN tasks.due_date IS 'Optional due date for the task';",

            # Add reminder_time column (optional datetime field)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP WITH TIME ZONE;",
            "COMMENT ON COLUMN tasks.reminder_time IS 'Optional reminder time for the task';",

            # Add recurrence_type column (optional, max 20 chars)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_type VARCHAR(20);",
            "COMMENT ON COLUMN tasks.recurrence_type IS 'Recurrence pattern: daily, weekly, monthly';",

            # Add recurrence_metadata column (optional, max 500 chars)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_metadata VARCHAR(500);",
            "COMMENT ON COLUMN tasks.recurrence_metadata IS 'Additional recurrence data';",

            # Update existing records to set default priority if they have NULL values
            "UPDATE tasks SET priority = 'Medium' WHERE priority IS NULL;"
        ]

        cursor = conn.cursor()
        print("Connected successfully. Executing migration statements...")

        for statement in alter_statements:
            print(f"Executing: {statement}")
            cursor.execute(statement)
            conn.commit()  # Commit each statement individually to avoid issues

        print("Successfully added missing columns to tasks table!")
        print("The tasks table now includes: priority, due_date, reminder_time, recurrence_type, recurrence_metadata")

        # Verify the columns were added
        cursor.execute("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = 'tasks' AND column_name IN ('priority', 'due_date', 'reminder_time', 'recurrence_type', 'recurrence_metadata');")
        results = cursor.fetchall()
        print("\nVerification - New columns added:")
        for col in results:
            print(f"  {col[0]}: {col[1]}, nullable: {col[2]}, default: {col[3]}")

        cursor.close()
        conn.close()
        print("\nMigration completed successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise

if __name__ == "__main__":
    print("Starting database migration to add missing task columns...")
    print("This may take a few moments to connect to the database...")
    start_time = time.time()
    add_missing_task_columns()
    end_time = time.time()
    print(f"\nMigration completed in {end_time - start_time:.2f} seconds!")