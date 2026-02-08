
# Intermediate Todo App Upgrade Plan

## 1. Updated Data Model
```typescript
type Priority = 'High' | 'Medium' | 'Low';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  createdAt: Date;
  dueDate?: Date;
}

type FilterStatus = 'All' | 'Pending' | 'Completed';
type FilterPriority = 'All' | Priority;
```

## 2. State & Derived Values
- `tasks: Task[]` - Main task list
- `newTaskTitle: string` - Current input for new task title
- `newTaskDescription: string` - Current input for new task description
- `newTaskPriority: Priority` - Current input for new task priority
- `newTaskTags: string` - Current input for new task tags (comma-separated)
- `searchTerm: string` - Current search term
- `statusFilter: FilterStatus` - Current status filter
- `priorityFilter: FilterPriority` - Current priority filter
- `tagFilter: string` - Current tag filter ('All' or specific tag)
- `sortOption: string` - Current sort option
- `sortDirection: 'asc' | 'desc'` - Current sort direction

For computing filtered/sorted tasks: Create a `getFilteredAndSortedTasks()` function that applies search, filters, and sorting in sequence to the main tasks array.

LocalStorage sync: Use useEffect to save tasks to localStorage whenever the tasks array changes.

## 3. UI Layout Suggestion
- **Header/Add Form**: Contains the input fields for adding new tasks (title, description, priority dropdown, tags input) and add button
- **Controls Section**: Contains search input, status filter dropdown, priority filter dropdown, tag filter dropdown, and sort dropdown
- **Task List**: Displays tasks as cards with checkboxes, titles, priority badges (color-coded), tag badges, descriptions, and delete buttons
- **Stats Footer**: Shows total tasks and currently showing count

## 4. Step-by-Step Implementation Order
**1.1: Update Task interface** (XS, 5–10 min)
Add priority, tags, createdAt fields to the Task interface.

**1.2: Initialize new state variables** (S, 10–15 min)
Add useState hooks for priority, tags, filters, search, and sort options.

**2.1: Update addTask function** (S, 15–20 min)
Modify the function to accept and store priority, tags, and createdAt.

**2.2: Create tag parsing utility** (XS, 5–10 min)
Function to convert comma-separated string to array of trimmed tags.

**3.1: Add priority dropdown to form** (XS, 5–10 min)
Add a select element for priority selection in the task creation form.

**3.2: Add tags input field** (XS, 5–10 min)
Add an input field for entering comma-separated tags.

**4.1: Display priority badges** (XS, 10–15 min)
Show priority as color-coded badges on task cards (red=High, yellow=Medium, green=Low).

**4.2: Display tag badges** (S, 15–20 min)
Show tags as blue badges/chips on task cards.

**5.1: Implement search functionality** (S, 20–25 min)
Add search input and logic to filter tasks by title/description.

**5.2: Implement status filter** (S, 15–20 min)
Add dropdown to filter tasks by completion status.

**6.1: Implement priority filter** (S, 15–20 min)
Add dropdown to filter tasks by priority level.

**6.2: Implement tag filter** (M, 25–30 min)
Add dynamic dropdown showing all unique tags for filtering.

**7.1: Implement sorting functionality** (M, 30–40 min)
Add sort dropdown with options for date, priority, and alphabetical sorting.

**7.2: Add localStorage synchronization** (S, 15–20 min)
Set up useEffect to save tasks to localStorage when they change.

**8.1: Add edit task functionality** (L, 45–60 min)
Implement ability to edit existing tasks with pre-filled values.

**8.2: Handle edge cases and empty states** (S, 20–25 min)
Show appropriate messages when no tasks exist or search/filter returns no results.

## 5. Key Functions to Implement
- `addTask`: Creates new task with priority, tags, createdAt
- `toggleComplete`: Updates task completion status
- `deleteTask`: Removes task from list
- `getFilteredAndSortedTasks`: Applies all filters and sorting to tasks
- `handleSearchChange`: Updates search term state
- `parseTags`: Converts comma-separated string to tag array
- `getUniqueTags`: Returns all unique tags from tasks for filter dropdown
- `editTask`: Updates existing task with new values

## 6. Edge Cases & Gotchas to Watch
- No tasks → show welcome message
- Empty search/filter result → show "No matching tasks" message
- Duplicate tags → normalize and deduplicate tags
- Special characters in search → use case-insensitive matching
- Sorting after filtering → apply filters first, then sort
- localStorage parse errors → wrap JSON.parse in try-catch with fallback
- Priority color logic consistent (red=High, yellow=Medium, green=Low)
- Empty tag input → don't add empty tags to task
- Multiple consecutive commas in tag input → handle gracefully
- Leading/trailing spaces in tags → trim tags
- Case sensitivity in tag filtering → normalize case for comparison
- Date comparison for sorting → convert to timestamp for reliable comparison

## 7. Milestones for Testing
- After step 1.2: State variables are initialized and accessible
- After step 2.1: Tasks can be added with priority and tags
- After step 4.2: Priority and tag badges display correctly
- After step 5.1: Real-time search filters tasks by keyword
- After step 6.2: All filter types work correctly
- After step 7.1: Tasks sort correctly by selected criteria
- After step 8.1: Tasks can be edited with pre-filled values

## 8. Final Polish Ideas
- Clear filters button to reset all active filters
- Smooth animations when adding/removing tasks
- Keyboard shortcuts for common actions
- Responsive design adjustments for mobile screens
- Confirmation dialog for task deletion
- Visual feedback when saving to localStorage

## 9. Next Level Teaser (after this)
- Drag-and-drop reordering of tasks
- Due date reminders and notifications
- Categories as collapsible sidebar
- Export tasks to CSV/JSON
- Task sharing/collaboration features