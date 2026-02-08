# Quickstart Guide: Todo In-Memory Python Console App

## Setup

1. Ensure Python 3.13+ is installed on your system
2. Install uv package manager if not already installed:
   ```
   pip install uv
   ```
3. Create a virtual environment:
   ```
   uv venv
   ```
4. Activate the virtual environment:
   - On Windows: `Scripts\activate` (in the venv directory)
5. Navigate to the project directory

## Running the Application

1. From the project root directory, run:
   ```
   python src/main.py
   ```

## Using the Application

Once the application is running, you can use the following commands:

- `add <title> [description]` - Add a new task with the given title and optional description
- `list` or `view` - Display all tasks with their status
- `update <id> [new_title] [new_description]` - Update the title and/or description of a task
- `delete <id>` - Delete a task by its ID
- `mark <id>` - Toggle the completion status of a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Example Usage

```
> add Buy groceries Milk and eggs needed
Task added successfully! ID: 1

> add Walk the dog
Task added successfully! ID: 2

> list
ID | Status | Title           | Description
1  | [ ]    | Buy groceries   | Milk and eggs needed
2  | [ ]    | Walk the dog    | 

> mark 1
Task 1 marked as Complete

> list
ID | Status | Title           | Description
1  | [X]    | Buy groceries   | Milk and eggs needed
2  | [ ]    | Walk the dog    | 

> quit
Goodbye!
```