# AI-Powered Task Manager for Umama

An intelligent, proactive personal AI task manager & life assistant built for Umama.

## Features

- Natural language task creation (e.g., "roz subah gym", "har Monday meeting 10 AM")
- Smart recurring tasks with exception handling
- Intelligent reminders and notifications
- Automatic priority detection
- Task categorization
- Urdu-English code-switching support
- Persistent storage (simulated with JSON files)
- Overdue task detection and highlighting
- Logging functionality for debugging and monitoring

## Prerequisites

- Python 3.13 or higher
- pip package manager

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
4. Run the application:
   ```bash
   cd src
   python main.py
   ```

## Usage

The AI assistant understands natural language inputs:

```
> roz subah gym
Task "gym" added as daily recurring task for morning time.

> har Monday meeting 10 AM
Task "meeting" added as weekly recurring task for Mondays at 10 AM.

> kal dopahar 2 baje doctor appointment
Task "doctor appointment" added for tomorrow at 2 PM.
```

### Available Commands

- `add <task_description>` - Add a task using natural language
- `list [all|pending|completed|overdue|<category>]` - List tasks with optional filtering
- `complete <task_number_or_title>` - Mark a task as completed
- `skip <task_number_or_title>` - Skip a recurring task instance
- `delete <task_number_or_title>` - Delete a task
- `help` - Show help information
- `quit` or `exit` - Exit the application

### Natural Language Examples

The system understands various natural language expressions:

- **Task Creation**: "roz subah gym", "har Monday meeting 10 AM", "kal dopahar 2 baje doctor appointment"
- **Priority Indicators**: "urgent meeting with boss", "asap submit report", "zaroori grocery shopping"
- **Recurring Tasks**: "har roz exercise", "har month bill pay", "har 2 weeks haircut"
- **Reminders**: "remind me 1 day before meeting", "remind me 30 min before appointment"
- **Categories**: "work project deadline", "health checkup", "personal shopping"

### Task Priorities

The system automatically detects task priority based on keywords:
- 🔥 **High**: "urgent", "asap", "immediately", "zaroori"
- 🟡 **Medium**: "soon", "this week", "this month"
- 🟢 **Low**: Default for tasks without priority indicators

### Task Categories

Tasks are automatically categorized based on content:
- **Work**: "office", "meeting", "project", "report", "client"
- **Study**: "exam", "book", "course", "assignment", "class"
- **Personal**: "family", "home", "shopping", "appointment"
- **Health**: "doctor", "gym", "exercise", "meditation", "hospital"
- **Finance**: "bill", "payment", "money", "budget", "expense"

## Architecture

The application follows a modular architecture with the following components:

- **Models**: Task, RecurrencePattern, ReminderSettings, UserProfile
- **Services**: NLP processing, Task creation, Recurrence handling, Notifications, Priority detection
- **CLI Interface**: Command-line interface for user interaction
- **Storage**: In-memory with persistent JSON backup

## Logging

The application logs important events to the `logs/` directory. Log files are created daily with the format `taskmanager_YYYYMMDD.log`.

## License

MIT