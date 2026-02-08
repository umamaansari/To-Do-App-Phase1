# Data Model: Todo In-Memory Python Console App

## Entities

### Task
Represents a single todo item with the following attributes:

- **id** (int): Unique identifier for the task, auto-generated sequentially
- **title** (str): Required title of the task
- **description** (str): Optional description of the task
- **completed** (bool): Boolean indicating whether the task is completed (default: False)

### Example Task
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False
}
```

## Relationships
None - this is a simple application with a single entity type.

## Validation Rules
- id: Must be a positive integer, unique across all tasks
- title: Required, must not be empty
- description: Optional, can be any string
- completed: Must be a boolean value

## State Transitions
Tasks can transition between two states:
- Pending (completed = False)
- Complete (completed = True)

The toggle operation switches between these two states.