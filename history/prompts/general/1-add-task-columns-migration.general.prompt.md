---
id: 1
title: "Add Missing Task Columns Migration"
stage: "tasks"
date_iso: "2026-02-18"
surface: "agent"
model: "Claude Opus 4.6"
feature: "none"
branch: "main"
user: "user"
command: "add missing task columns migration"
labels: ["database", "migration", "sqlmodel", "postgresql"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "add_missing_task_columns.sql"
  - "add_task_columns_migration.py"
  - "alembic_task_migration.py"
  - ".env.example"
tests_yaml: []
---

# Add Missing Task Columns Migration

## User Prompt
My FastAPI + SQLModel backend is running but GET /api/tasks/ fails with:

psycopg2.errors.UndefinedColumn: column tasks.priority does not exist

The Task model includes new fields:
priority, due_date, reminder_time, recurrence_type, recurrence_metadata

Generate the correct PostgreSQL ALTER TABLE queries to safely update the existing tasks table schema without dropping data.

## Assistant Response
Generated the correct PostgreSQL ALTER TABLE queries and migration scripts to add missing columns to the tasks table:

- Created `add_missing_task_columns.sql` with raw ALTER TABLE statements
- Created `add_task_columns_migration.py` for programmatic migration execution
- Created `alembic_task_migration.py` template for proper migration tracking
- Updated `.env.example` to fix DATABASE_URL variable name
- Used IF NOT EXISTS clauses to safely add columns without data loss
- Set appropriate default values for new columns

The migration adds the missing columns: priority, due_date, reminder_time, recurrence_type, and recurrence_metadata to match the Task model definition.

## Outcome
Successfully resolved the database schema mismatch that was causing the UndefinedColumn error. The migration scripts provide multiple approaches to safely update the database schema while preserving existing data.