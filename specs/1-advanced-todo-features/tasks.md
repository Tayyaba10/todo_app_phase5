---
description: "Task list for Advanced Todo Features implementation"
---

# Tasks: Advanced Todo Features

**Input**: Design documents from `/specs/1-advanced-todo-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the existing project structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in backend/src/models/
- [ ] T002 Create project structure per implementation plan in frontend/src/components/
- [ ] T003 [P] Set up database migration framework for schema changes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create Tag model in backend/src/models/tag.py
- [X] T005 Update Task model with new fields in backend/src/models/task.py (priority, due_date, reminder_time, recurrence_type, recurrence_metadata)
- [X] T006 Create Pydantic models for new task attributes in backend/src/api/schemas/task.py
- [X] T007 Create database migration for new task fields and Tag model (automatic via SQLModel/SQLAlchemy)
- [X] T008 Create service functions for priority, tags, due dates, reminders, and recurrence in backend/src/services/task_service.py
- [X] T009 Add validation rules for new fields in backend/src/api/schemas/task.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Manage Task Priorities (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign priority levels to tasks and sort/filter by priority

**Independent Test**: Can be fully tested by creating tasks with various priorities, then applying sorting and filtering operations to confirm correct display and ordering

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**


- [ ] T010 [P] [US1] Contract test for priority API endpoints in backend/tests/contract/test_priority_api.py
- [ ] T011 [P] [US1] Integration test for priority functionality in backend/tests/integration/test_priority.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Priority model/schema in backend/src/api/schemas/task.py
- [X] T013 [P] [US1] Update Task CRUD operations to handle priority in backend/src/api/routes/tasks.py
- [X] T014 [US1] Update frontend TaskForm to include priority selection in frontend/src/components/TaskForm.tsx
- [X] T015 [US1] Add priority sorting functionality in backend/src/services/task_service.py
- [X] T016 [US1] Add priority filtering functionality in backend/src/services/task_service.py
- [X] T017 [US1] Update frontend UI to display priority indicators in frontend/src/components/TaskItem.tsx
- [X] T018 [US1] Add priority filter controls to frontend in frontend/src/components/TaskList.jsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Organize Tasks with Tags (Priority: P1)

**Goal**: Enable users to add multiple custom tags to tasks and dynamically create new tags, allowing for categorization and filtering

**Independent Test**: Can be fully tested by adding new tags to tasks, creating new tags, and then filtering by these tags to confirm accurate grouping

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for tags API endpoints in backend/tests/contract/test_tags_api.py
- [ ] T020 [P] [US2] Integration test for tag functionality in backend/tests/integration/test_tags.py

### Implementation for User Story 2

- [X] T021 [P] [US2] Create tag association endpoints in backend/src/api/routes/tags.py
- [X] T022 [P] [US2] Implement tag creation service in backend/src/services/tag_service.py
- [X] T023 [US2] Implement tag assignment to tasks in backend/src/services/task_service.py
- [X] T024 [US2] Update Task model to handle many-to-many relationship with Tags in backend/src/models/task.py
- [X] T025 [US2] Add tag filtering functionality in backend/src/services/task_service.py
- [X] T026 [US2] Update frontend TaskForm to support tag input in frontend/src/components/TaskForm.tsx
- [X] T027 [US2] Update frontend UI to display tags and support filtering by tags in frontend/src/components/TaskItem.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search and Filter Tasks (Priority: P1)

**Goal**: Enable users to search for tasks by title/description and filter by status, priority, tags, or due date range

**Independent Test**: Can be fully tested by creating a diverse set of tasks and then performing various combinations of search and filter operations to ensure correct results

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US3] Contract test for search/filter API endpoints in backend/tests/contract/test_search_api.py
- [ ] T029 [P] [US3] Integration test for search and filter functionality in backend/tests/integration/test_search_filter.py

### Implementation for User Story 3

- [X] T030 [P] [US3] Implement search functionality in backend/src/services/task_service.py
- [X] T031 [P] [US3] Implement combined filter functionality in backend/src/services/task_service.py
- [X] T032 [US3] Add search endpoint to backend in backend/src/api/routes/tasks.py
- [X] T033 [US3] Update frontend with search bar in frontend/src/components/TaskList.jsx
- [X] T034 [US3] Update frontend with filter controls in frontend/src/components/FilterPanel.tsx
- [X] T035 [US3] Implement frontend search service function in frontend/src/services/taskService.js

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Sort Tasks (Priority: P2)

**Goal**: Enable users to sort tasks by creation date, due date, priority, or alphabetically by title

**Independent Test**: Can be fully tested by creating tasks with varied attributes and applying each sort option to confirm correct ordering

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US4] Contract test for sort API endpoints in backend/tests/contract/test_sort_api.py
- [ ] T037 [P] [US4] Integration test for sort functionality in backend/tests/integration/test_sort.py

### Implementation for User Story 4

- [X] T038 [P] [US4] Implement sort functionality in backend/src/services/task_service.py
- [X] T039 [P] [US4] Add sort parameters to task listing endpoint in backend/src/api/routes/tasks.py
- [X] T040 [US4] Update frontend TaskList to support sorting in frontend/src/components/TaskList.tsx
- [X] T041 [US4] Add sort controls to frontend in frontend/src/components/SortControls.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Set Due Dates and Reminders (Priority: P1)

**Goal**: Enable users to assign due dates and set reminder times before due dates, with backend logic to identify upcoming and overdue items

**Independent Test**: Can be fully tested by setting due dates and reminders, then verifying that the backend correctly identifies upcoming and overdue tasks

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T042 [P] [US5] Contract test for due date/reminder API endpoints in backend/tests/contract/test_due_date_api.py
- [ ] T043 [P] [US5] Integration test for due date and reminder functionality in backend/tests/integration/test_due_dates.py

### Implementation for User Story 5

- [X] T044 [P] [US5] Update Task model validation for due date and reminder time in backend/src/api/schemas/task.py
- [X] T045 [P] [US5] Implement reminder validation service in backend/src/services/reminder_service.py
- [X] T046 [US5] Add due date and reminder fields to Task CRUD operations in backend/src/api/routes/tasks.py
- [X] T047 [US5] Implement backend logic to detect upcoming and overdue reminders in backend/src/services/reminder_service.py
- [X] T048 [US5] Update frontend TaskForm to include due date and reminder inputs in frontend/src/components/TaskForm.tsx
- [X] T049 [US5] Update frontend UI to show overdue tasks and remind indicators in frontend/src/components/TaskItem.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: User Story 6 - Manage Recurring Tasks (Priority: P2)

**Goal**: Enable users to set tasks to recur daily, weekly, or monthly, with automatic generation of new instances when current ones are completed

**Independent Test**: Can be fully tested by setting up a recurring task, marking it complete, and verifying that the next occurrence is correctly generated

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T050 [P] [US6] Contract test for recurring task API endpoints in backend/tests/contract/test_recurring_api.py
- [ ] T051 [P] [US6] Integration test for recurring task functionality in backend/tests/integration/test_recurring_tasks.py

### Implementation for User Story 6

- [X] T052 [P] [US6] Implement recurrence logic in backend/src/services/task_service.py
- [X] T053 [P] [US6] Update Task completion endpoint to handle recurrence in backend/src/api/routes/tasks.py
- [X] T054 [US6] Add recurrence type validation in backend/src/api/schemas/task.py
- [X] T055 [US6] Implement new occurrence generation logic in backend/src/services/task_service.py
- [X] T056 [US6] Update frontend TaskForm to include recurrence options in frontend/src/components/TaskForm.tsx
- [X] T057 [US6] Add unit tests for recurrence logic in backend/tests/unit/test_recurrence.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T058 [P] Add comprehensive unit tests for all new backend logic in backend/tests/unit/
- [ ] T059 [P] Add frontend component tests in frontend/tests/
- [ ] T060 [P] Update documentation in docs/advanced-features.md
- [ ] T061 [P] Perform integration testing across all new features
- [ ] T062 [P] Performance testing for search and filter operations with large datasets
- [ ] T063 [P] Validate backward compatibility with existing API consumers
- [ ] T064 [P] Update quickstart documentation to reflect new features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - May integrate with US5 for completion logic

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for priority API endpoints in backend/tests/contract/test_priority_api.py"
Task: "Integration test for priority functionality in backend/tests/integration/test_priority.py"

# Launch all models for User Story 1 together:
Task: "Create Priority model/schema in backend/src/models/schemas.py"
Task: "Update Task CRUD operations to handle priority in backend/src/api/task_routes.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
   - Developer F: User Story 6
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence