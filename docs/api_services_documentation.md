# API and Services Documentation: AI-Powered Task Manager for Umama

## Overview
This document provides an overview of the main APIs and services in the AI-Powered Task Manager application.

## Core Services

### 1. TaskStore Service
**Location**: `src/services/task_store.py`

**Purpose**: Manages in-memory storage of tasks, users, recurrence patterns, and reminder settings with optional persistent backup.

**Key Methods**:
- `add_task(task)`: Add a new task to the store
- `get_task(task_id)`: Retrieve a task by its ID
- `update_task(task)`: Update an existing task
- `delete_task(task_id)`: Delete a task by its ID
- `get_tasks_by_status(status)`: Retrieve tasks by status
- `get_tasks_by_priority(priority)`: Retrieve tasks by priority
- `get_tasks_by_category(category)`: Retrieve tasks by category
- `get_all_tasks()`: Retrieve all tasks

### 2. NaturalLanguageProcessor Service
**Location**: `src/services/nlp_service.py`

**Purpose**: Processes natural language input to extract task information including title, due dates, recurrence patterns, priority, and category.

**Key Methods**:
- `process_task_input(text)`: Process natural language input and extract task information
- `_extract_title(text)`: Extract the task title from input text
- `_extract_recurrence_pattern(text)`: Extract recurrence pattern from input text
- `_extract_reminder_settings(text)`: Extract reminder preferences from input text
- `_determine_priority(text)`: Determine task priority based on keywords
- `_determine_category(text)`: Determine task category based on keywords

### 3. TaskCreationService
**Location**: `src/services/task_creation_service.py`

**Purpose**: Orchestrates task creation from natural language input by coordinating with NLP processor and task store.

**Key Methods**:
- `create_task_from_natural_language(text)`: Create a task from natural language input
- `_create_recurrence_pattern(task, pattern_data)`: Create and store a recurrence pattern for the task
- `_create_reminder_settings(task, reminder_data)`: Create and store reminder settings for the task

### 4. RecurrenceService
**Location**: `src/services/recurrence_service.py`

**Purpose**: Manages recurring tasks and their patterns, including generating next occurrences and handling exceptions.

**Key Methods**:
- `generate_next_occurrence(pattern)`: Generate the next occurrence date based on the recurrence pattern
- `handle_completed_recurring_task(task)`: Handle a completed recurring task by creating the next occurrence
- `skip_recurring_task_instance(task)`: Skip a recurring task instance and schedule the next one

### 5. NotificationService
**Location**: `src/services/notification_service.py`

**Purpose**: Manages notifications and reminders for tasks based on user preferences.

**Key Methods**:
- `set_notification_callback(callback)`: Set the callback function for notifications
- `schedule_notification(reminder_settings, task_title)`: Schedule a notification based on reminder settings
- `_calculate_notification_time(reminder_settings)`: Calculate when the notification should be sent
- `_trigger_notification(message, reminder_settings)`: Trigger the notification

### 6. PriorityDetectionService
**Location**: `src/services/priority_detection.py`

**Purpose**: Detects and suggests task priorities based on keywords and other factors.

**Key Methods**:
- `detect_priority_from_text(text)`: Detect priority level based on keywords in the text
- `suggest_priority(task)`: Suggest a priority for a task based on its content and other factors
- `apply_priority_suggestion(task)`: Apply a priority suggestion to a task if it doesn't already have a priority

### 7. CategoryDetectionService
**Location**: `src/services/category_detection.py`

**Purpose**: Detects and suggests task categories based on content.

**Key Methods**:
- `detect_category_from_text(text)`: Detect category based on keywords in the text
- `suggest_category(task)`: Suggest a category for a task based on its content
- `apply_category_suggestion(task)`: Apply a category suggestion to a task if it doesn't already have a category

## Models

### 1. Task Model
**Location**: `src/models/task.py`

**Attributes**:
- `id`: Unique identifier for the task
- `title`: Task name/title
- `description`: Detailed description
- `due_date`: Specific due date and time
- `status`: Task status (pending, completed, skipped)
- `priority`: Task priority (high, medium, low)
- `category`: Task category
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated
- `completed_at`: Timestamp when task was completed
- `notes`: Additional notes or comments
- `recurrence_pattern`: Recurrence details
- `reminder_settings`: Reminder preferences
- `estimated_duration`: Estimated time in minutes to complete the task

### 2. RecurrencePattern Model
**Location**: `src/models/recurrence.py`

**Attributes**:
- `id`: Unique identifier for the pattern
- `task_id`: Reference to the associated task
- `pattern_type`: Type of recurrence (daily, weekly, monthly, yearly, custom)
- `interval`: How often the pattern repeats
- `days_of_week`: Days of week for weekly patterns
- `day_of_month`: Day of month for monthly patterns
- `exceptions`: Specific dates to skip
- `end_condition`: When the recurrence ends
- `next_occurrence`: When the next instance is due

### 3. ReminderSettings Model
**Location**: `src/models/reminder_settings.py`

**Attributes**:
- `id`: Unique identifier for the settings
- `task_id`: Reference to the associated task
- `method`: Method of reminder (notification, email, sms)
- `timing`: When to send the reminder (at_due_time, before_due, custom)
- `minutes_before`: Minutes before due time
- `enabled`: Whether reminders are active for this task
- `last_reminder_sent`: When the last reminder was sent

### 4. UserProfile Model
**Location**: `src/models/user_profile.py`

**Attributes**:
- `id`: Unique identifier for the user
- `timezone`: User's timezone
- `language_preference`: Preferred language
- `notification_preferences`: User's notification settings
- `created_at`: When the profile was created
- `updated_at`: When the profile was last updated
- `last_active`: When the user was last active
- `ai_model_preferences`: Preferences for AI behavior and suggestions

## CLI Interface

### CLIInterface
**Location**: `src/cli/interface.py`

**Commands**:
- `add <task_description>`: Add a task using natural language
- `list [all|pending|completed|overdue|<category>]`: List tasks with optional filtering
- `complete <task_number_or_title>`: Mark a task as completed
- `skip <task_number_or_title>`: Skip a recurring task instance
- `delete <task_number_or_title>`: Delete a task
- `help`: Show help information
- `quit` or `exit`: Exit the application

## Persistent Storage

### PersistentStorage
**Location**: `src/lib/persistent_storage.py`

**Purpose**: Simple persistent storage simulation using JSON files.

**Key Methods**:
- `save_tasks(tasks)`: Save tasks to the tasks file
- `load_tasks()`: Load tasks from the tasks file
- `save_users(users)`: Save users to the users file
- `load_users()`: Load users from the users file

## Logging

### Logger
**Location**: `src/lib/logger.py`

**Purpose**: Simple logging functionality for debugging and monitoring.

**Key Methods**:
- `info(message)`: Log an info message
- `warning(message)`: Log a warning message
- `error(message)`: Log an error message
- `debug(message)`: Log a debug message