import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta
from src.services.task_service import TaskService

def test_daily_recurrence():
    """Test daily recurrence calculation."""
    current_date = datetime(2023, 1, 1, 10, 0, 0)
    next_occurrence = TaskService._calculate_next_occurrence(current_date, "daily")

    expected = current_date + timedelta(days=1)
    assert next_occurrence == expected
    print("✓ Daily recurrence test passed")


def test_weekly_recurrence():
    """Test weekly recurrence calculation."""
    current_date = datetime(2023, 1, 1, 10, 0, 0)  # Sunday
    next_occurrence = TaskService._calculate_next_occurrence(current_date, "weekly")

    expected = current_date + timedelta(days=7)
    assert next_occurrence == expected
    print("✓ Weekly recurrence test passed")


def test_monthly_recurrence():
    """Test monthly recurrence calculation."""
    current_date = datetime(2023, 1, 1, 10, 0, 0)
    next_occurrence = TaskService._calculate_next_occurrence(current_date, "monthly")

    # Moving to next month - handling different month lengths
    expected = datetime(2023, 2, 1, 10, 0, 0)
    assert next_occurrence == expected
    print("✓ Monthly recurrence test passed")


def test_monthly_recurrence_edge_case():
    """Test monthly recurrence with edge case (e.g., Jan 31 to Feb)."""
    current_date = datetime(2023, 1, 31, 10, 0, 0)
    next_occurrence = TaskService._calculate_next_occurrence(current_date, "monthly")

    # Feb doesn't have 31 days, so it should go to the last day of Feb
    expected = datetime(2023, 2, 28, 10, 0, 0)
    assert next_occurrence == expected
    print("✓ Monthly recurrence edge case test passed")


def test_invalid_recurrence_type():
    """Test invalid recurrence type returns None."""
    current_date = datetime(2023, 1, 1, 10, 0, 0)
    next_occurrence = TaskService._calculate_next_occurrence(current_date, "invalid")

    assert next_occurrence is None
    print("✓ Invalid recurrence type test passed")


def test_no_current_due_date():
    """Test when no current due date is provided."""
    next_occurrence = TaskService._calculate_next_occurrence(None, "daily")

    assert next_occurrence is None
    print("✓ No current due date test passed")


if __name__ == "__main__":
    print("Running recurrence tests...")
    test_daily_recurrence()
    test_weekly_recurrence()
    test_monthly_recurrence()
    test_monthly_recurrence_edge_case()
    test_invalid_recurrence_type()
    test_no_current_due_date()
    print("All tests passed! ✅")