---
id: 2
title: "Intermediate Todo App Implementation Plan"
stage: plan
date_iso: 2026-02-05
surface: agent
model: Qwen
feature: todo-enhancements
branch: 001-todo-enhancements
user: DELL
command: sp.plan
labels: ["planning", "architecture", "react", "todo-app"]
links:
  spec: "specs/1-todo-enhancements/spec.md"
  plan: "specs/001-todo-enhancements/plan.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-todo-enhancements/plan.md"
  - "specs/001-todo-enhancements/research.md"
  - "specs/001-todo-enhancements/data-model.md"
  - "specs/001-todo-enhancements/quickstart.md"
  - "specs/001-todo-enhancements/contracts/task-api.md"
tests_yaml: []
prompt_text: |
  User's current app: Basic Todo already done (add task with title + description, toggle complete, delete, show list, localStorage save/load). Code is in single App.tsx file using React + TypeScript + Tailwind CSS + hooks (useState + useEffect).

  Now upgrade to intermediate level with exactly these features:

  Core new features:
  1. Priority: High / Medium / Low – dropdown on add/edit, color-coded badges (red/yellow/green)
  2. Tags/Categories: multiple tags per task (comma-separated input), show as blue badges/chips, allow custom tags
  3. Search: real-time search input (filter title + description)
  4. Filters:
     - Status: All / Pending / Completed
     - Priority: All / High / Medium / Low
     - Tag: dynamic dropdown of all existing unique tags + "All"
  5. Sorting: dropdown with options
     - Created date (newest/oldest)
     - Priority (High→Low or Low→High)
     - Alphabetical (A→Z or Z→A)

  Optional nice-to-have (include if easy, but not mandatory):
  - Due date field (simple date input, sort by due date also)
  - Basic edit task (click task → modal or inline edit with pre-filled values)

  Rules & preferences:
  - Keep using React + TypeScript + functional components + hooks
  - Use Tailwind CSS for styling (keep clean, modern cards/lists)
  - State management: useState + useEffect only (no Context/Zustand yet)
  - All data in localStorage (update after add/edit/delete/complete)
  - Client-side filtering, searching, sorting (no backend)
  - Handle empty states, no results messages
  - Make UI responsive (mobile-friendly)

  Your task: Create a **detailed implementation PLAN** for this upgrade.

  Output structure (follow exactly this format, use markdown):

  # Intermediate Todo App Upgrade Plan

  ## 1. Updated Data Model
  Show full TypeScript interface for Task (include all fields like id, title, description?, completed, priority, tags: string[], createdAt, dueDate? etc.)
  Any extra types (e.g. Priority type)

  ## 2. State & Derived Values
  - List all useState variables needed
  - How to compute filtered/sorted tasks (explain logic briefly)
  - How localStorage sync works

  ## 3. UI Layout Suggestion
  Describe high-level layout:
  - Header / Add form
  - Controls (search + filters + sort dropdowns)
  - Task list (cards with checkbox, title, priority badge, tags, description, delete)
  - Stats (total / showing count)

  ## 4. Step-by-Step Implementation Order
  Numbered list (12–18 steps), realistic order with dependencies.
  Each step format:
  - **Step X.Y: Short Title** (difficulty: XS/S/M/L, time est: ~min)
    - What to do (specific changes: add field, create function, update JSX etc.)
    - Why this order / dependencies
    - Key code snippet idea (1–4 lines max)

  Example:
  **3.1: Update Task interface** (XS, 5–10 min)
  Add priority, tags, createdAt fields...

  ## 5. Key Functions to Implement
  List important handler functions with brief purpose:
  - addTask
  - toggleComplete
  - deleteTask
  - getFilteredAndSortedTasks (derived)
  - handleSearchChange, etc.

  ## 6. Edge Cases & Gotchas to Watch
  Bullet list of 10+ important things:
  - No tasks → show message
  - Empty search/filter result
  - Duplicate tags
  - Special characters in search
  - Sorting after filtering
  - localStorage parse errors (JSON.parse safe)
  - Priority color logic consistent

  ## 7. Milestones for Testing
  After which steps you can test meaningful parts:
  - After step X: priorities show & colors work
  - After step Y: search filters in real-time
  - etc.

  ## 8. Final Polish Ideas
  Small touches to make it feel premium:
  - Clear filters button
  - Animate new task add
  - Dark mode toggle (optional)
  - Confirm delete (optional)

  ## 9. Next Level Teaser (after this)
  2–3 advanced ideas (drag-drop reorder, due date reminders, categories as sidebar etc.)

  Generate the full plan now. Be detailed, practical, and opinionated where it improves UX/code quality.
  Tips for best result:

  Agar due date nahi chahiye → prompt mein "Optional nice-to-have" section se due date line hata dena.
  Agar edit task abhi nahi chahiye → us line ko bhi comment out kar dena.
  Prompt ke end mein agar apna current App.tsx code paste kar dena to plan uske hisaab se adapt ho jayega (better accuracy).
response_text: |
  Created a comprehensive implementation plan for upgrading the basic todo app to intermediate level with priorities, tags, search, filter, and sort functionality. The plan includes:
  1. Updated data model with Task interface
  2. State management approach using useState hooks
  3. UI layout suggestions
  4. Step-by-step implementation order (18 steps)
  5. Key functions to implement
  6. Edge cases to consider
  7. Testing milestones
  8. Polish ideas
  9. Future enhancement ideas

  Additionally created supporting documents:
  - Research documentation
  - Data model specification
  - API contracts
  - Quickstart guide
outcome: |
  Successfully created detailed implementation plan and supporting documentation for the intermediate todo app upgrade. All required artifacts have been generated in the appropriate directory structure.
evaluation: |
  The plan comprehensively covers all requested features with a logical implementation sequence. Supporting documents provide additional clarity on data models, API contracts, and setup instructions. The plan follows best practices for React development with TypeScript.
---

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
- `sortDirection: 'asc' | 'desc` - Current sort direction

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