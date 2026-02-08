# Data Model for Intermediate Todo App

## Task Entity
Represents a single task with enhanced properties

**Fields:**
- `id: string` - Unique identifier for the task
- `title: string` - Task title/name
- `description?: string` - Optional task description
- `completed: boolean` - Completion status
- `priority: 'High' | 'Medium' | 'Low'` - Task priority level
- `tags: string[]` - Array of tag strings for categorization
- `createdAt: Date` - Timestamp when task was created
- `dueDate?: Date` - Optional due date for the task

**Validation Rules:**
- `id` must be unique across all tasks
- `title` must not be empty
- `priority` must be one of 'High', 'Medium', or 'Low'
- `tags` array elements must not be empty strings after trimming
- `createdAt` must be a valid date
- `dueDate` if present must be a valid date

## Filter Types
**FilterStatus:** 'All' | 'Pending' | 'Completed'
**FilterPriority:** 'All' | 'High' | 'Medium' | 'Low'

## State Variables
- `tasks: Task[]` - Main collection of all tasks
- `newTaskTitle: string` - Temporary storage for new task title
- `newTaskDescription: string` - Temporary storage for new task description
- `newTaskPriority: Priority` - Temporary storage for new task priority
- `newTaskTags: string` - Temporary storage for new task tags (comma-separated)
- `searchTerm: string` - Current search term for filtering
- `statusFilter: FilterStatus` - Current status filter selection
- `priorityFilter: FilterPriority` - Current priority filter selection
- `tagFilter: string` - Current tag filter ('All' or specific tag)
- `sortOption: string` - Current sort option (e.g., 'createdDate', 'priority', 'alphabetical')
- `sortDirection: 'asc' | 'desc'` - Current sort direction