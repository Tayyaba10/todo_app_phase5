---
id: 1
title: UUID Error Fix in Task-Tag Association Table
stage: general
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: tayya
command: "fix uuid error"
labels: ["bug-fix", "sqlalchemy", "uuid", "models"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - D:\todo_app_phase5\backend\src\models\task_tag.py
tests:
 - none
---

## Prompt

solve this error
uvicorn src.main:app --reload
INFO:     Will watch for changes in these directories: ['D:\\todo_app_phase5\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [5944] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\schema.py", line 226, in _init_items
    spwd = item._set_parent_with_dispatch
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: type object 'UUID' has no attribute '_set_parent_with_dispatch'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\uvicorn\_subprocess.py", line 76, in subprocess_started
    target(sockets=sockets)
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\uvicorn\server.py", line 61, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\uvicorn\server.py", line 68, in serve
    config.load()
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\uvicorn\config.py", line 467, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\uvicorn\importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "D:\todo_app_phase5\backend\src\main.py", line 13, in <module>
    from src.api.routes import tasks
  File "D:\todo_app_phase5\backend\src\api\routes\tasks.py", line 5, in <module>
    from ..deps import get_current_user
  File "D:\todo_app_phase5\backend\src\api\deps.py", line 5, in <module>
    from ..models.user import User
  File "D:\todo_app_phase5\backend\src\models\__init__.py", line 3, in <module>
    from .task import Task
  File "D:\todo_app_phase5\backend\src\models\task.py", line 12, in <module>
    from .task_tag import task_tag_association_table
  File "D:\todo_app_phase5\backend\src\models\task_tag.py", line 13, in <module>
    Column("task_id", UUID, ForeignKey("tasks.id")),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\schema.py", line 2167, in __init__
    self._init_items(*cast(_typing_Sequence[SchemaItem], l_args))
  File "C:\Users\tayya\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\schema.py", line 228, in _init_items
    raise exc.ArgumentError(
sqlalchemy.exc.ArgumentError: 'SchemaItem' object, such as a 'Column' or a 'Constraint' expected, got <class 'uuid.UUID'>

## Response snapshot

The error occurred because in the `task_tag.py` file, Python's built-in `UUID` class was being used directly in SQLAlchemy's `Column` definition. SQLAlchemy expected a proper SQLAlchemy schema item, but received Python's `uuid.UUID` type instead, causing the AttributeError.

I fixed this by updating `D:\todo_app_phase5\backend\src\models\task_tag.py`:
1. Added import for PostgreSQL UUID type: `from sqlalchemy.dialects.postgresql import UUID as PostgresUUID`
2. Updated the association table to use the proper SQLAlchemy UUID type:
   - `Column("task_id", PostgresUUID(as_uuid=True), ForeignKey("tasks.id"))` - for task_id which references UUID primary key in tasks table
   - `Column("tag_id", ForeignKey("tags.id"))` - kept as default type since Tag uses integer primary key

The error has been resolved and the application should now start successfully with `uvicorn src.main:app --reload`.

## Outcome

- ✅ Impact: Fixed SQLAlchemy UUID error that prevented application startup
- 🧪 Tests: none
- 📁 Files: Updated models/task_tag.py to use proper PostgresUUID type in association table
- 🔁 Next prompts: none
- 🧠 Reflection: When using SQLAlchemy with UUID columns, the proper SQLAlchemy UUID type must be used instead of Python's UUID class

## Evaluation notes (flywheel)

- Failure modes observed: Application failed to start due to incorrect UUID type usage
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A