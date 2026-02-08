---
id: 1
title: Todo App Constitution
stage: constitution
date_iso: 2026-02-05
surface: agent
model: Qwen
feature: todo-app
branch: main
user: DELL
command: /sp.constitution
labels:
  - constitution
  - todo-app
  - python
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
prompt_text: |
  /sp.constitution Project Constitution: Todo In-Memory Python Console App (Phase 1)

  Project Overview
  Build a basic command-line Todo application in Python that manages tasks completely in memory (no file or database persistence in this phase). 
  The application must support the 5 core features: Add, Delete, Update, View, Mark as Complete/Incomplete.
  Development must follow spec-driven approach using Spec-Kit Plus.
  Use Qwen (or similar) to help refine specifications or generate initial code skeletons from this constitution.
  Follow clean code principles and standard Python project structure.

  Main Objectives
  - Create a minimal viable Todo console app for hackathon demonstration
  - Show spec-driven development workflow: constitution → detailed specs → code implementation
  - Keep everything simple, fast to build, and easy to demo in terminal
  - No data should be saved after program exits (pure in-memory)

  Technology Stack
  - Python: 3.13 or newer
  - Package / environment manager: uv
  - Specification tool: Spec-Kit Plus
  - AI assistance: Qwen (for spec generation, refinement, code ideas)
  - External dependencies: none / minimal (only built-in modules preferred)

  Core Features - Must Implement Exactly These
  1. Add Task
     - User can create new task with title (required) and description (optional)
     - Automatically assign unique incremental ID (starting from 1)
     - Initial status: not completed
     - Show confirmation with the assigned ID

  2. Delete Task
     - Delete task by entering its ID
     - Show error message if ID does not exist
     - Show success message after deletion

  3. Update Task
     - Update title and/or description of existing task by ID
     - Allow partial update (only title, only description, or both)
     - Show error if ID not found
     - Show updated task details after change

  4. View / List Tasks
     - Show all current tasks in a readable format
     - Display for each task: ID, Title, Description, Status (Complete / Pending)
     - Use simple indicators e.g. [X] Completed   [ ] Pending
     - If no tasks → show friendly message "No tasks yet."

  5. Mark as Complete / Incomplete
     - Toggle completion status of a task by ID
     - One command should toggle (complete ↔ incomplete)
     - Show error if ID not found
     - Show new status after toggle

  Additional Must-Have Behaviors
  - Command-line interface runs in a loop
  - User types commands like: add, list, update, delete, mark, help, quit
  - Support simple 'help' command showing available commands
  - 'quit' or 'exit' should close the application gracefully
  - Handle invalid inputs gracefully (show error message, don't crash)
  - IDs must be integers and unique

  Data Structure Recommendation (in-memory only)
  - Use a list of dictionaries
  - Example task: {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "completed": False}

  Project Structure (required)
  - src/
    - main.py               → CLI loop and user interaction
    - todo_manager.py       → class or functions for task logic
  - spec_history/           → folder to save all generated .spec or .json specification versions
  - constitution.txt        → this file
  - README.md               → setup instructions + usage examples

  Spec-Driven Development Rules
  1. Use this constitution as the root document
  2. Feed this text to Spec-Kit Plus + Qwen to generate first detailed specification file
  3. Save generated spec in spec_history/ (v1.spec, v2.spec, etc.)
  4. Implement code based on the latest spec version
  5. If requirements change slightly → create new spec version, do not break existing working features

  Success Criteria for Phase 1
  - Application runs without crashing
  - All 5 features work correctly
  - Clean, readable console output
  - GitHub repo contains:
    - constitution file
    - spec history folder with at least 1-2 spec files
    - src folder with working code
    - README with:
      - How to install uv (if needed)
      - How to create virtual env and run the app
      - Example commands with screenshots or text samples
response_text: |
  Created a comprehensive project constitution for the Todo In-Memory Python Console App. The constitution includes six core principles (Minimalist Design, Console-First Interface, Test-First, Memory-Only Persistence, Error Handling, Clean Code Standards), additional constraints covering technology stack and data structure requirements, development workflow guidelines, and governance rules. The constitution follows the required format with proper versioning (1.0.0), ratification date (2026-02-05), and last amended date (2026-02-05). All requirements from the user's specification have been incorporated into the constitution document.
outcome: 
evaluation: 
---

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Minimalist Design
Every feature should serve a clear purpose with minimal complexity; implementations must be simple, readable, and maintainable; Focus on core functionality without over-engineering solutions.

### II. Console-First Interface
The application must provide a clean command-line interface; Text-based input/output protocol: user commands → console display; Support human-readable formats with clear prompts and feedback.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all functionality.

### IV. Memory-Only Persistence
All data remains in memory during application runtime; No file or database persistence required; Data is lost when application terminates; Focus on core logic without persistence complexity.

### V. Error Handling
Robust error handling required: Invalid inputs handled gracefully, clear error messages displayed, application must not crash due to user errors; Defensive programming practices enforced.

### VI. Clean Code Standards
Code must follow Python PEP 8 standards; Functions should be small and focused; Meaningful variable and function names; Proper documentation for complex logic.

## Additional Constraints

Technology stack requirements:
- Python: 3.13 or newer
- Package/environment manager: uv
- External dependencies: none/minimal (only built-in modules preferred)
- Project structure: src/, spec_history/, README.md, constitution file

Data structure requirements:
- Use a list of dictionaries for task storage
- Each task: {"id": int, "title": str, "description": str, "completed": bool}
- IDs must be integers and unique, starting from 1

Core features that must be implemented:
- Add Task: Create new task with title (required) and description (optional)
- Delete Task: Delete task by entering its ID
- Update Task: Update title and/or description of existing task by ID
- View/List Tasks: Show all current tasks in a readable format
- Mark as Complete/Incomplete: Toggle completion status of a task by ID

## Development Workflow

- Use spec-driven development: constitution → detailed specs → code implementation
- Save generated spec files in spec_history/ folder
- Implement code based on the latest spec version
- Support simple 'help' command showing available commands
- 'quit' or 'exit' should close the application gracefully
- Handle invalid inputs gracefully (show error message, don't crash)

## Governance

This constitution serves as the foundational document for the Todo In-Memory Python Console App project; All development activities must comply with these principles; Amendments require documentation and team approval; All pull requests must verify compliance with these principles; Simplicity must be prioritized over complexity.

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05