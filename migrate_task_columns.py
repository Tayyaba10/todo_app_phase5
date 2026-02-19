"""
Database migration script to add missing columns to tasks table
This script uses raw SQL to add the new fields without dropping existing data
"""
import asyncio
from sqlmodel import create_engine, Session
from backend.src.core.config import settings
from backend.src.models.task import Task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_missing_columns():
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)

    with Session(engine) as session:
        # Execute raw SQL to add missing columns
        queries = [
            # Add priority column with default value
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'Medium';",

            # Add due_date column (optional datetime field)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;",

            # Add reminder_time column (optional datetime field)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP WITH TIME ZONE;",

            # Add recurrence_type column (optional, max 20 chars)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_type VARCHAR(20);",

            # Add recurrence_metadata column (optional, max 500 chars)
            "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_metadata VARCHAR(500);",

            # Update existing records to set default priority if they have NULL values
            "UPDATE tasks SET priority = 'Medium' WHERE priority IS NULL;",
        ]

        try:
            for query in queries:
                logger.info(f"Executing: {query}")
                session.exec(query)

            session.commit()
            logger.info("Successfully added missing columns to tasks table")

        except Exception as e:
            logger.error(f"Error adding missing columns: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    add_missing_columns()