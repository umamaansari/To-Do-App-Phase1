# Quickstart Guide: AI-Powered Task Manager for Umama

## Overview
This guide will help you get started with the AI-Powered Task Manager for Umama. The application features natural language processing for task creation, smart scheduling, and proactive notifications.

## Prerequisites
- Python 3.13 or higher
- pip package manager
- Virtual environment tool (recommended: venv or uv)

## Setup Instructions

### 1. Clone or Create the Project Structure
```bash
mkdir ai-task-manager
cd ai-task-manager
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install spacy parsedatetime pytz langdetect python-dateutil
python -m spacy download en_core_web_sm  # For English NLP
```

### 4. Initialize the Application
Create the main application file structure:

```
ai-task-manager/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── recurrence.py
│   │   └── user_profile.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── nlp_service.py
│   │   ├── task_service.py
│   │   ├── scheduler.py
│   │   └── notification_service.py
│   └── cli/
│       ├── __init__.py
│       └── interface.py
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   └── test_nlp.py
├── data/
│   └── tasks.json  # In-memory storage simulation
└── README.md
```

## Basic Usage

### Starting the Application
```bash
cd src
python main.py
```

### Adding Tasks with Natural Language
The AI assistant understands natural language inputs:

```
> roz subah gym
Task "gym" added as daily recurring task for morning time.

> har Monday meeting 10 AM
Task "meeting" added as weekly recurring task for Mondays at 10 AM.

> kal dopahar 2 baje doctor appointment
Task "doctor appointment" added for tomorrow at 2 PM.
```

### Managing Tasks
```
> list tasks
• **gym** | 🔁 Daily | 🟢 Low | 📅 Tomorrow 7:00 AM
• **meeting** | 🔁 Weekly | 🟡 Medium | 📅 Next Monday 10:00 AM
• **doctor appointment** | 📅 Tomorrow 2:00 PM | 🟡 Medium

> complete doctor appointment
Task "doctor appointment" marked as completed.

> skip next Monday meeting
Next Monday's "meeting" task has been skipped.
```

### Setting Reminders
```
> remind me 1 day before doctor appointment
Reminder set: 1 day before "doctor appointment".

> remind me 30 min before meeting
Reminder set: 30 minutes before "meeting".
```

## Key Features

### 1. Natural Language Processing
The system parses natural language inputs to extract:
- Task titles and descriptions
- Due dates and times
- Recurrence patterns
- Priority levels
- Categories

### 2. Recurring Tasks
Support for various recurrence patterns:
- Daily, weekly, monthly, yearly
- Custom intervals (every 3 days, every 2 weeks)
- Exception handling (skip specific dates)

### 3. Smart Prioritization
Automatic priority detection based on keywords:
- "urgent", "asap", "immediately" → High priority
- "soon", "this week" → Medium priority
- Default → Low priority

### 4. Proactive Notifications
Timely reminders based on user preferences:
- At due time
- Before due time (configurable)
- Custom timing

## Configuration
The application uses a user profile to store preferences:
- Timezone (defaults to Pakistan)
- Language preferences (Urdu-English mix)
- Notification settings
- Default categories and priorities

## Troubleshooting

### Common Issues
1. **NLP parsing fails**: Ensure spaCy models are downloaded
2. **Date/time confusion**: Check that your system timezone matches Pakistan time
3. **Commands not recognized**: Check spelling and try simpler phrases

### Getting Help
Type `help` or `commands` to see all available commands.