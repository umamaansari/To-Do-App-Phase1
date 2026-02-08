# Data Model: AI-Powered Task Manager for Umama

## Overview
This document defines the data structures and relationships for the AI-Powered Task Manager for Umama, based on the feature requirements and entities identified in the specification.

## Core Entities

### Task
Represents a single task with all its attributes and metadata.

```python
{
    "id": "uuid-string",                    # Unique identifier for the task
    "title": "string",                      # Task name/title (in English for clarity)
    "description": "string",                # Detailed description (can be in Urdu/English)
    "due_date": "datetime",                 # Specific due date and time
    "status": "enum",                       # Values: "pending", "completed", "skipped"
    "priority": "enum",                     # Values: "high", "medium", "low"
    "category": "string",                   # Category: "work", "study", "personal", "health", "finance"
    "created_at": "datetime",               # Timestamp when task was created
    "updated_at": "datetime",               # Timestamp when task was last updated
    "completed_at": "datetime",             # Timestamp when task was completed (null if not completed)
    "notes": "string",                      # Additional notes or comments
    "recurrence_pattern": "dict",           # Recurrence details (see below)
    "reminder_settings": "dict",            # Reminder preferences (see below)
    "estimated_duration": "integer"         # Estimated time in minutes to complete the task
}
```

Validation rules:
- id must be unique and follow UUID format
- title is required and must not exceed 200 characters
- status must be one of the allowed values
- priority must be one of the allowed values
- due_date must be a valid datetime object
- estimated_duration must be positive if provided

### RecurrencePattern
Defines how a task repeats over time.

```python
{
    "id": "uuid-string",                    # Unique identifier for the pattern
    "task_id": "uuid-string",               # Reference to the associated task
    "pattern_type": "enum",                 # Values: "daily", "weekly", "monthly", "yearly", "custom"
    "interval": "integer",                  # How often the pattern repeats (e.g., every 2 weeks)
    "days_of_week": "list",                 # Days of week for weekly patterns (0=Monday, 6=Sunday)
    "day_of_month": "integer",              # Day of month for monthly patterns (1-31)
    "exceptions": "list",                   # Specific dates to skip (list of date strings)
    "end_condition": "dict",                # When the recurrence ends (see below)
    "next_occurrence": "datetime",          # When the next instance is due
    "created_at": "datetime",               # When the pattern was created
    "updated_at": "datetime"                # When the pattern was last updated
}
```

Validation rules:
- task_id must reference a valid task
- interval must be positive
- days_of_week values must be between 0-6
- day_of_month must be between 1-31
- exceptions must be valid date strings

### EndCondition
Specifies when a recurring task should stop repeating.

```python
{
    "type": "enum",                         # Values: "after_occurrences", "on_date", "never"
    "count": "integer",                     # Number of occurrences (for "after_occurrences")
    "date": "date"                          # Specific end date (for "on_date")
}
```

Validation rules:
- If type is "after_occurrences", count must be positive
- If type is "on_date", date must be a valid date

### ReminderSettings
Configures when and how the user is reminded about a task.

```python
{
    "id": "uuid-string",                    # Unique identifier for the settings
    "task_id": "uuid-string",               # Reference to the associated task
    "method": "enum",                       # Values: "notification", "email", "sms"
    "timing": "enum",                       # Values: "at_due_time", "before_due", "custom"
    "minutes_before": "integer",            # Minutes before due time (for "before_due" and "custom")
    "enabled": "boolean",                   # Whether reminders are active for this task
    "last_reminder_sent": "datetime"        # When the last reminder was sent
}
```

Validation rules:
- task_id must reference a valid task
- minutes_before must be positive for "before_due" and "custom" timing
- enabled must be boolean

### UserProfile
Stores user preferences and persistent data.

```python
{
    "id": "uuid-string",                    # Unique identifier for the user
    "timezone": "string",                   # User's timezone (e.g., "Asia/Karachi")
    "language_preference": "string",        # Preferred language (e.g., "urdu-english")
    "notification_preferences": "dict",     # User's notification settings
    "created_at": "datetime",               # When the profile was created
    "updated_at": "datetime",               # When the profile was last updated
    "last_active": "datetime",              # When the user was last active
    "ai_model_preferences": "dict"          # Preferences for AI behavior and suggestions
}
```

Validation rules:
- timezone must be a valid IANA timezone
- language_preference must be one of supported combinations

## Relationships

### Task and RecurrencePattern
- One-to-One relationship: Each recurring task has exactly one recurrence pattern
- Foreign key: RecurrencePattern.task_id references Task.id
- Cascade delete: When a task is deleted, its recurrence pattern is also deleted

### Task and ReminderSettings
- One-to-One relationship: Each task has zero or one reminder setting
- Foreign key: ReminderSettings.task_id references Task.id
- Cascade delete: When a task is deleted, its reminder settings are also deleted

### Task and UserProfile
- Many-to-One relationship: Multiple tasks belong to one user
- Foreign key: Task.user_id references UserProfile.id (not shown in Task model above but assumed)
- Cascade delete: When a user profile is deleted, all associated tasks are also deleted

## State Transitions

### Task Status Transitions
- `pending` → `completed`: When user marks task as done
- `pending` → `skipped`: When user skips a recurring task instance
- `completed` → `pending`: When user reopens a completed task
- `skipped` → `pending`: When user decides to reschedule a skipped task

### Task Priority Updates
- Priority can be updated at any time based on AI suggestions or user input
- Priority changes may affect task ordering in views

## Indexes for Performance

For efficient querying, the following indexes should be created:

1. Task.due_date: For sorting and filtering by due date
2. Task.status: For filtering by completion status
3. Task.priority: For sorting by priority
4. Task.category: For filtering by category
5. Task.created_at: For chronological ordering
6. RecurrencePattern.next_occurrence: For identifying upcoming recurring tasks
7. UserProfile.timezone: For user-specific queries