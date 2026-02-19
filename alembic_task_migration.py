"""
Migration script for adding missing task columns using alembic

This migration adds the advanced features fields to the tasks table:
- priority
- due_date
- reminder_time
- recurrence_type
- recurrence_metadata
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_add_task_advanced_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add priority column
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), server_default='Medium', nullable=False))

    # Add due_date column
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(timezone=True), nullable=True))

    # Add reminder_time column
    op.add_column('tasks', sa.Column('reminder_time', sa.DateTime(timezone=True), nullable=True))

    # Add recurrence_type column
    op.add_column('tasks', sa.Column('recurrence_type', sa.String(length=20), nullable=True))

    # Add recurrence_metadata column
    op.add_column('tasks', sa.Column('recurrence_metadata', sa.String(length=500), nullable=True))

    # Update existing records to ensure consistent default values
    # op.execute("UPDATE tasks SET priority = 'Medium' WHERE priority IS NULL")


def downgrade():
    # Remove columns in reverse order
    op.drop_column('tasks', 'recurrence_metadata')
    op.drop_column('tasks', 'recurrence_type')
    op.drop_column('tasks', 'reminder_time')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')