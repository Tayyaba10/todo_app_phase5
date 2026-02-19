#!/usr/bin/env python3
"""
Test script to verify the UUID error fix in the task_tag.py model
"""

def test_imports():
    try:
        print("Testing import of task_tag model...")
        from src.models.task_tag import task_tag_association_table
        print("✓ task_tag_association_table imported successfully")

        print("Testing import of main models...")
        from src.models import User, Task, Tag
        print("✓ User, Task, and Tag models imported successfully")

        print("Testing import of main app...")
        from src.main import app
        print("✓ Main app imported successfully")

        print("\n🎉 All imports successful! The UUID error has been fixed.")
        return True
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()