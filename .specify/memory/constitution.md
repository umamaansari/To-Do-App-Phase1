<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: Core Principles for Todo App, Additional Constraints, Development Workflow
Removed sections: N/A
Templates requiring updates: N/A (new project)
Follow-up TODOs: None
-->

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