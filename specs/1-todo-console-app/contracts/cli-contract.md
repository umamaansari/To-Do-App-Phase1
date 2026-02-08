# Todo App CLI Interface Contract

## Overview
This document specifies the command-line interface for the Todo In-Memory Python Console App. It defines the commands, their syntax, expected inputs, and outputs.

## Command Syntax

### Add Task
```
add <title> [description]
```

**Description**: Adds a new task with the given title and optional description.

**Parameters**:
- `title` (required): The title of the task
- `description` (optional): A description of the task

**Response**:
- Success: "Task added successfully! ID: <id>"
- Error: "Title is required." if title is empty

### List Tasks
```
list
```
or
```
view
```

**Description**: Displays all tasks with their status.

**Response**:
- Success: Formatted table of all tasks with ID, Status, Title, and Description
- Empty: "No tasks yet."

### Update Task
```
update <id> [new_title] [new_description]
```

**Description**: Updates the title and/or description of an existing task.

**Parameters**:
- `id` (required): The ID of the task to update
- `new_title` (optional): The new title for the task
- `new_description` (optional): The new description for the task

**Response**:
- Success: "Task <id> updated successfully!"
- Error: "Task with ID <id> not found." if ID doesn't exist

### Delete Task
```
delete <id>
```

**Description**: Deletes a task by its ID.

**Parameters**:
- `id` (required): The ID of the task to delete

**Response**:
- Success: "Task <id> deleted."
- Error: "Task with ID <id> not found." if ID doesn't exist

### Mark Task
```
mark <id>
```

**Description**: Toggles the completion status of a task.

**Parameters**:
- `id` (required): The ID of the task to mark

**Response**:
- Success: "Task <id> marked as [Completed/Pending]."
- Error: "Task with ID <id> not found." if ID doesn't exist

### Help
```
help
```

**Description**: Shows available commands with brief descriptions.

**Response**:
- List of all available commands with descriptions

### Quit
```
quit
```
or
```
exit
```

**Description**: Exits the application.

**Response**:
- "Goodbye!"