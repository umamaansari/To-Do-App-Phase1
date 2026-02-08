---
description: "Task list template for feature implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/1-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src/ directory structure per implementation plan
- [X] T002 Create spec_history/ directory for versioned spec files
- [X] T003 [P] Create initial README.md with setup instructions from quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create base TodoManager class in src/todo_manager.py with basic structure
- [X] T005 [P] Define Task data model in src/todo_manager.py based on data-model.md
- [X] T006 [P] Create CLI loop structure in src/main.py with basic command parsing
- [ ] T007 Create error handling utilities in src/utils.py (if needed)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list with a title and optional description

**Independent Test**: Can be fully tested by running the app, entering the 'add' command with a title and description, and verifying that a new task appears in the list with a unique ID.

### Implementation for User Story 1

- [X] T008 [P] [US1] Implement add_task method in src/todo_manager.py with ID generation logic
- [X] T009 [P] [US1] Add validation for required title in src/todo_manager.py
- [X] T010 [US1] Implement 'add' command handler in src/main.py
- [X] T011 [US1] Add user feedback for successful task addition in src/main.py
- [ ] T012 [US1] Test add functionality with title only (no description)
- [ ] T013 [US1] Test add functionality with both title and description

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Allow users to see all their tasks with their status so they can understand what they need to do and what they've completed

**Independent Test**: Can be fully tested by adding a few tasks and then using the 'list' command to see all tasks with their status indicators.

### Implementation for User Story 2

- [X] T014 [P] [US2] Implement get_all_tasks method in src/todo_manager.py
- [X] T015 [US2] Implement 'list'/'view' command handler in src/main.py
- [X] T016 [US2] Format output with ID, title, description, and status indicators per research decision
- [X] T017 [US2] Handle empty list case with friendly message "No tasks yet."
- [ ] T018 [US2] Test list functionality with multiple tasks showing [X] and [ ] indicators
- [ ] T019 [US2] Test empty list case

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Allow users to update the title or description of existing tasks so they can keep their task information accurate

**Independent Test**: Can be fully tested by adding a task, updating its details, and verifying the changes appear when viewing the task list.

### Implementation for User Story 3

- [X] T020 [P] [US3] Implement find_task_by_id helper method in src/todo_manager.py
- [X] T021 [US3] Implement update_task method in src/todo_manager.py allowing partial updates
- [X] T022 [US3] Implement 'update' command handler in src/main.py with hybrid input approach
- [X] T023 [US3] Add error handling for invalid task IDs in src/todo_manager.py
- [ ] T024 [US3] Test update functionality with title only, description only, and both
- [ ] T025 [US3] Test update functionality with invalid ID

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Allow users to mark tasks as complete or incomplete so they can track their progress

**Independent Test**: Can be fully tested by adding a task, marking it complete, verifying the status changed, then marking it incomplete again.

### Implementation for User Story 4

- [X] T026 [P] [US4] Implement toggle_complete method in src/todo_manager.py
- [X] T027 [US4] Implement 'mark' command handler in src/main.py
- [X] T028 [US4] Add user feedback for status changes in src/main.py
- [ ] T029 [US4] Test toggle functionality from pending to complete
- [ ] T030 [US4] Test toggle functionality from complete back to pending
- [ ] T031 [US4] Test mark functionality with invalid ID

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Allow users to remove tasks they no longer need so their todo list stays relevant

**Independent Test**: Can be fully tested by adding a task, deleting it, and verifying it no longer appears in the task list.

### Implementation for User Story 5

- [X] T032 [P] [US5] Implement delete_task method in src/todo_manager.py
- [X] T033 [US5] Implement 'delete' command handler in src/main.py
- [X] T034 [US5] Add user feedback for successful deletion in src/main.py
- [ ] T035 [US5] Test delete functionality with valid ID
- [ ] T036 [US5] Test delete functionality with invalid ID
- [ ] T037 [US5] Test delete functionality with last remaining task

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Additional Commands & Error Handling

**Goal**: Implement remaining required commands and comprehensive error handling

- [X] T038 [P] Implement 'help' command showing all available commands in src/main.py
- [X] T039 [P] Implement 'quit'/'exit' command handlers in src/main.py
- [X] T040 Add comprehensive error handling for invalid command syntax per spec
- [X] T041 Handle non-existent task IDs for update/delete/mark operations
- [X] T042 Handle empty title error when adding tasks
- [X] T043 Handle very long titles/descriptions appropriately
- [X] T044 Add type hints to all methods per implementation guidelines
- [X] T045 Add docstrings to all classes and methods per implementation guidelines

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T046 [P] Documentation updates in README.md with usage examples
- [X] T047 Code cleanup and refactoring following PEP 8 style
- [X] T048 Manual testing against all acceptance criteria from spec.md
- [X] T049 [P] Manual testing of full task lifecycle (add → view → update → mark → delete)
- [X] T050 Run quickstart validation per plan.md requirements

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Additional Commands**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tasks for User Story 1 together:
Task: "Implement add_task method in src/todo_manager.py with ID generation logic"
Task: "Add validation for required title in src/todo_manager.py"
Task: "Implement 'add' command handler in src/main.py"
Task: "Add user feedback for successful task addition in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence