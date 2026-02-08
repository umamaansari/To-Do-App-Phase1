# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `1-todo-console-app` | **Date**: 2026-02-05 | **Spec**: [link]
**Input**: Feature specification from `/specs/1-todo-console-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a command-line Todo application in Python that stores tasks in memory. The app implements 5 core features: Add, Delete, Update, View/List, and Mark Complete/Incomplete. The architecture follows a clean separation between CLI interface (main.py) and business logic (todo_manager.py).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Built-in modules only (sys, os, typing)
**Storage**: In-memory only (list of dictionaries)
**Testing**: Manual testing against acceptance criteria
**Target Platform**: Console/terminal application
**Project Type**: Single executable console application
**Performance Goals**: Instant response in terminal (sub-second for all operations)
**Constraints**: <100MB memory usage, no external dependencies, no file persistence
**Scale/Scope**: Single user, up to 100 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Minimalist Design: Implementation will be simple and focused
- ✅ Console-First Interface: Text-based input/output protocol
- ✅ Test-First (NON-NEGOTIABLE): Manual tests will be performed against acceptance criteria
- ✅ Memory-Only Persistence: All data remains in memory during runtime
- ✅ Error Handling: Robust error handling with user-friendly messages
- ✅ Clean Code Standards: Following PEP 8 standards with type hints

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-console-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # CLI loop and user interaction
└── todo_manager.py      # Task logic class

tests/
└── manual_test_cases.md # Manual test cases based on spec

spec_history/
└── v1-todo-spec.md      # Generated spec file
```

**Structure Decision**: Single project structure chosen to keep the implementation simple and focused on the core functionality. The modular design separates concerns between the CLI interface and the business logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## 1. Overview and Confirmed Tech Stack

The Todo In-Memory Python Console App will be built using:
- Python 3.13+ as the primary language
- Built-in modules only (no external dependencies)
- In-memory storage using a list of dictionaries
- Command-line interface for user interaction
- uv for virtual environment management

## 2. Text-based Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Todo Console App                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐     ┌──────────────────────────────┐   │
│  │   CLI Loop      │     │     TodoManager Class        │   │
│  │   (main.py)     │────▶│                              │   │
│  │                 │     │ • add_task()                 │   │
│  │ • Input/Output  │     │ • delete_task()              │   │
│  │ • Command Parse │     │ • update_task()              │   │
│  │ • Dispatch      │     │ • get_all_tasks()            │   │
│  │                 │     │ • toggle_complete()          │   │
│  └─────────────────┘     │ • find_task_by_id()          │   │
│                          │                              │   │
│                          │ • tasks: List[Dict]          │   │
│                          │   (in-memory storage)        │   │
│                          └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 3. Important Architectural and Design Decisions

### 3.1 Command Parsing Method
- **Options Considered**:
  - A) Simple input().strip().split() with manual checks
  - B) Use argparse module
  - C) Use shlex for better argument handling
- **Chosen**: A) Simple split
- **Tradeoffs**: Zero dependencies, very fast to write, good enough for MVP, less robust for quoted strings (not needed here)

### 3.2 Task Storage Structure
- **Options Considered**:
  - A) list[dict] with sequential append
  - B) dict[int, dict] with ID as key
- **Chosen**: A) list[dict]
- **Tradeoffs**: Easy to loop and sort for list command, ID generation simple

### 3.3 ID Generation Logic
- **Options Considered**:
  - A) len(self.tasks) + 1 after append
  - B) Find max existing ID + 1 (handles deletes better)
- **Chosen**: B) max + 1
- **Tradeoffs**: IDs remain dense even after deletes, very small performance cost

### 3.4 Update Command Input Style
- **Options Considered**:
  - A) Only accept full arguments: update <id> <title> <desc>
  - B) Interactive: ask for title/desc if missing
- **Chosen**: Hybrid - try arguments first, if not enough then prompt interactively
- **Tradeoffs**: Better user experience, still scriptable

### 3.5 List/View Output Formatting
- **Options Considered**:
  - A) Plain print with f-strings and fixed width
  - B) Use external table library like tabulate
- **Chosen**: A) f-strings
- **Tradeoffs**: No deps, clean enough for console, easy alignment

## 4. Detailed Module and File Breakdown

### 4.1 src/main.py
The main entry point of the application that handles:
- The infinite CLI loop
- Reading user input
- Parsing commands
- Calling appropriate TodoManager methods
- Formatting and printing output
- Graceful exit handling

### 4.2 src/todo_manager.py
Contains the TodoManager class that:
- Holds the task list in memory
- Implements all task manipulation methods
- Handles validation and error checking
- Maintains data integrity

## 5. Implementation Guidelines and Best Practices

- Use only built-in modules (typing for hints, sys if needed)
- Implement exception handling: ValueError for int(ID), KeyError/IndexError for bad ID, general Exception as fallback
- Console UX: "> " prompt, clear messages, separators between command outputs if needed
- Clean code: small functions, descriptive names, docstrings, type hints where useful
- Follow PEP 8 style guide
- Add type hints to all function signatures
- Include docstrings for classes and methods

## 6. Validation, Testing and Quality Strategy

- Manual testing against every acceptance criterion from the spec
- Test cases to cover:
  - Add: add with/without desc, check ID, status False, confirmation
  - List: empty list message, multiple tasks with [ ] / [X], long desc truncation if needed
  - Mark: toggle once, toggle twice (back to original), invalid ID error
  - Update: change title only, desc only, both, invalid ID
  - Delete: valid/invalid ID, delete from empty list
  - Edge: non-integer ID → catch ValueError, empty title on add → error
  - Full flow: add 3 tasks → list → update one → mark two → delete one → list → quit
- Quality checks: PEP8 style (manual or black if time permits), type hints on methods, docstrings, no crashes on bad input
- No unit tests required in Phase 1 (time constraint), focus on live console demo working perfectly

## 7. Potential Risks and How to Mitigate

- **Risk**: Memory usage grows too large with many tasks
  - **Mitigation**: Implement a warning when approaching 100 tasks limit
- **Risk**: User enters invalid commands repeatedly
  - **Mitigation**: Clear error messages and a 'help' command
- **Risk**: ID conflicts after many add/delete operations
  - **Mitigation**: Proper ID generation logic that finds next available ID
- **Risk**: Application crashes on unexpected input
  - **Mitigation**: Comprehensive error handling with try/catch blocks

## 8. Next Steps after this plan

1. Proceed to `/sp.tasks` to break this plan into specific implementation tasks
2. Begin implementation by creating the src/ directory and the two main files
3. Implement the TodoManager class first with all required methods
4. Implement the CLI loop in main.py
5. Test manually against all acceptance criteria
6. Refine and polish the user experience