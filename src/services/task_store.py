"""
TaskStore service for in-memory task storage with optional persistent backup.
"""
from typing import List, Optional, Dict, Any
from src.models.task import Task, TaskStatus, TaskPriority
from src.models.user_profile import UserProfile
from src.models.recurrence import RecurrencePattern
from src.models.reminder_settings import ReminderSettings
from src.lib.persistent_storage import PersistentStorage
from src.lib.logger import logger
import uuid


class TaskStore:
    """
    Service for managing in-memory task storage with persistent backup.
    """
    
    def __init__(self, use_persistent_storage: bool = True):
        self.tasks: Dict[str, Task] = {}
        self.users: Dict[str, UserProfile] = {}
        self.recurrence_patterns: Dict[str, RecurrencePattern] = {}
        self.reminder_settings: Dict[str, ReminderSettings] = {}
        
        if use_persistent_storage:
            self.persistent_storage = PersistentStorage()
            self._load_from_persistent_storage()
    
    def _load_from_persistent_storage(self):
        """Load tasks and users from persistent storage."""
        try:
            # Load tasks
            tasks_data = self.persistent_storage.load_tasks()
            for task_data in tasks_data:
                # Convert dict back to Task object
                task = Task(
                    id=task_data.get('id'),
                    title=task_data.get('title', ''),
                    description=task_data.get('description', ''),
                    due_date=task_data.get('due_date'),
                    status=TaskStatus(task_data.get('status')),
                    priority=TaskPriority(task_data.get('priority')),
                    category=task_data.get('category', ''),
                    created_at=task_data.get('created_at'),
                    updated_at=task_data.get('updated_at'),
                    completed_at=task_data.get('completed_at'),
                    notes=task_data.get('notes', ''),
                    recurrence_pattern=task_data.get('recurrence_pattern'),
                    reminder_settings=task_data.get('reminder_settings'),
                    estimated_duration=task_data.get('estimated_duration')
                )
                self.tasks[task.id] = task

            # Load users similarly if needed
            users_data = self.persistent_storage.load_users()
            for user_data in users_data:
                # Convert dict back to UserProfile object
                user = UserProfile(
                    id=user_data.get('id'),
                    timezone=user_data.get('timezone', 'Asia/Karachi'),
                    language_preference=user_data.get('language_preference', 'urdu-english'),
                    notification_preferences=user_data.get('notification_preferences', {}),
                    created_at=user_data.get('created_at'),
                    updated_at=user_data.get('updated_at'),
                    last_active=user_data.get('last_active'),
                    ai_model_preferences=user_data.get('ai_model_preferences', {})
                )
                self.users[user.id] = user

            logger.info(f"Loaded {len(self.tasks)} tasks and {len(self.users)} users from persistent storage")
        except Exception as e:
            logger.error(f"Could not load from persistent storage: {e}")
    
    def _save_to_persistent_storage(self):
        """Save tasks and users to persistent storage."""
        try:
            # Convert tasks to dictionaries
            tasks_data = [task.to_dict() for task in self.tasks.values()]
            self.persistent_storage.save_tasks(tasks_data)
            
            # Convert users to dictionaries
            users_data = [user.to_dict() for user in self.users.values()]
            self.persistent_storage.save_users(users_data)
            
            logger.info(f"Saved {len(self.tasks)} tasks and {len(self.users)} users to persistent storage")
        except Exception as e:
            logger.error(f"Could not save to persistent storage: {e}")
    
    def add_task(self, task: Task) -> Task:
        """Add a new task to the store."""
        self.tasks[task.id] = task
        logger.info(f"Added task '{task.title}' with ID {task.id}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        task = self.tasks.get(task_id)
        if task:
            logger.info(f"Retrieved task '{task.title}' with ID {task_id}")
        else:
            logger.warning(f"Attempted to retrieve non-existent task with ID {task_id}")
        return task
    
    def update_task(self, task: Task) -> Task:
        """Update an existing task."""
        self.tasks[task.id] = task
        logger.info(f"Updated task '{task.title}' with ID {task.id}")
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            del self.tasks[task_id]
            # Also remove any associated recurrence pattern and reminder settings
            for pattern_id, pattern in list(self.recurrence_patterns.items()):
                if pattern.task_id == task_id:
                    del self.recurrence_patterns[pattern_id]
            
            for reminder_id, reminder in list(self.reminder_settings.items()):
                if reminder.task_id == task_id:
                    del self.reminder_settings[reminder_id]
            
            logger.info(f"Deleted task '{task.title}' with ID {task_id}")
            return True
        else:
            logger.warning(f"Attempted to delete non-existent task with ID {task_id}")
            return False
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Retrieve tasks by status."""
        tasks = [task for task in self.tasks.values() if task.status == status]
        logger.info(f"Retrieved {len(tasks)} tasks with status {status.value}")
        return tasks
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Retrieve tasks by priority."""
        tasks = [task for task in self.tasks.values() if task.priority.value == priority]
        logger.info(f"Retrieved {len(tasks)} tasks with priority {priority}")
        return tasks
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Retrieve tasks by category."""
        tasks = [task for task in self.tasks.values() if task.category.lower() == category.lower()]
        logger.info(f"Retrieved {len(tasks)} tasks in category '{category}'")
        return tasks
    
    def get_tasks_by_due_date_range(self, start_date: str, end_date: str) -> List[Task]:
        """Retrieve tasks by due date range."""
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        result = []
        for task in self.tasks.values():
            if task.due_date and start_dt <= task.due_date <= end_dt:
                result.append(task)
        logger.info(f"Retrieved {len(result)} tasks in date range {start_date} to {end_date}")
        return result
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        logger.info(f"Retrieved all {len(self.tasks)} tasks")
        return list(self.tasks.values())
    
    def add_user(self, user: UserProfile) -> UserProfile:
        """Add a new user to the store."""
        self.users[user.id] = user
        logger.info(f"Added user with ID {user.id}")
        return user
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve a user by ID."""
        user = self.users.get(user_id)
        if user:
            logger.info(f"Retrieved user with ID {user_id}")
        else:
            logger.warning(f"Attempted to retrieve non-existent user with ID {user_id}")
        return user
    
    def add_recurrence_pattern(self, pattern: RecurrencePattern) -> RecurrencePattern:
        """Add a recurrence pattern to the store."""
        self.recurrence_patterns[pattern.id] = pattern
        logger.info(f"Added recurrence pattern with ID {pattern.id}")
        return pattern
    
    def get_recurrence_pattern(self, pattern_id: str) -> Optional[RecurrencePattern]:
        """Retrieve a recurrence pattern by ID."""
        pattern = self.recurrence_patterns.get(pattern_id)
        if pattern:
            logger.info(f"Retrieved recurrence pattern with ID {pattern_id}")
        else:
            logger.warning(f"Attempted to retrieve non-existent recurrence pattern with ID {pattern_id}")
        return pattern
    
    def add_reminder_settings(self, reminder: ReminderSettings) -> ReminderSettings:
        """Add reminder settings to the store."""
        self.reminder_settings[reminder.id] = reminder
        logger.info(f"Added reminder settings with ID {reminder.id}")
        return reminder
    
    def get_reminder_settings(self, reminder_id: str) -> Optional[ReminderSettings]:
        """Retrieve reminder settings by ID."""
        reminder = self.reminder_settings.get(reminder_id)
        if reminder:
            logger.info(f"Retrieved reminder settings with ID {reminder_id}")
        else:
            logger.warning(f"Attempted to retrieve non-existent reminder settings with ID {reminder_id}")
        return reminder
    
    def get_reminder_settings_by_task(self, task_id: str) -> Optional[ReminderSettings]:
        """Retrieve reminder settings by task ID."""
        for reminder in self.reminder_settings.values():
            if reminder.task_id == task_id:
                logger.info(f"Retrieved reminder settings for task ID {task_id}")
                return reminder
        logger.warning(f"No reminder settings found for task ID {task_id}")
        return None