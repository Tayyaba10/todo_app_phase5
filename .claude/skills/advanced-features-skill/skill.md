---
name: advanced-features-skill
description: Implement advanced task management features including recurring tasks, due dates, reminders, priorities, tags, and search/filter/sort functionality.
---

# Advanced Features Skill

## Instructions

1. **Recurring Task Engine**
   - Define recurrence rules (daily, weekly, monthly, custom)
   - Store recurrence pattern in database
   - Automatically generate next occurrence
   - Handle completion without breaking recurrence chain

2. **Due Dates & Reminders**
   - Allow users to set due dates
   - Support reminder notifications (email / push / in-app)
   - Track overdue tasks
   - Enable snooze functionality

3. **Priorities & Tags**
   - Assign priority levels (low, medium, high)
   - Support multiple tags per task
   - Enable tag-based grouping
   - Display priority visually in UI

4. **Search, Filter & Sort**
   - Implement keyword-based search
   - Filter by status, priority, tags, due date
   - Sort by created date, due date, priority
   - Optimize queries for performance

## Best Practices
- Keep recurrence logic isolated from core task logic
- Use indexes for searchable fields
- Avoid heavy queries on large datasets
- Validate date formats consistently
- Maintain clear UI indicators for priority and overdue tasks
- Test edge cases for recurring tasks (leap year, timezone)

## Example Structure

### Task Model
```python
class Task(Base):
    id: int
    title: str
    description: str
    due_date: datetime
    priority: str
    is_recurring: bool
    recurrence_pattern: str
