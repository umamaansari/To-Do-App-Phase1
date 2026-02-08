# API Contract: Task Management

## Overview
This document describes the client-side API for managing tasks in the intermediate todo app. Since all operations happen in the browser, these represent the function interfaces and data structures used within the application.

## Data Structures

### Task Object
```json
{
  "id": "string",
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean",
  "priority": "'High' | 'Medium' | 'Low'",
  "tags": "string[]",
  "createdAt": "Date",
  "dueDate": "Date (optional)"
}
```

## Operations

### Create Task
**Function**: `addTask(taskData)`
- **Input**: Partial task object with at minimum a title
- **Output**: Updated task list with new task added
- **Behavior**: Adds new task to the list and saves to localStorage

### Read Tasks
**Function**: `getFilteredAndSortedTasks(filters)`
- **Input**: Object containing filter and sort parameters
- **Output**: Array of tasks matching the filters and sorted as requested
- **Behavior**: Applies all active filters and sorting to the task list

### Update Task
**Function**: `updateTask(id, updates)`
- **Input**: Task ID and object with fields to update
- **Output**: Updated task list with modified task
- **Behavior**: Finds task by ID and merges updates, then saves to localStorage

### Delete Task
**Function**: `deleteTask(id)`
- **Input**: Task ID
- **Output**: Updated task list without the deleted task
- **Behavior**: Removes task from list and saves to localStorage

### Toggle Completion
**Function**: `toggleTaskCompletion(id)`
- **Input**: Task ID
- **Output**: Updated task list with toggled completion status
- **Behavior**: Flips the completed status of the specified task and saves to localStorage

## Client-Side Storage
All data is persisted using the browser's localStorage API with the key "todo-app-tasks". The stored value is a JSON string representing the array of Task objects.