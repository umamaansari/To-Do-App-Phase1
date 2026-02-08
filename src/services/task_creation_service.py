"""
TaskCreationService to orchestrate task creation.
"""
from typing import Dict, Any, Optional
from src.models.task import Task, TaskPriority
from src.models.recurrence import RecurrencePattern, EndCondition, EndConditionType
from src.models.reminder_settings import ReminderSettings
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_store import TaskStore


class TaskCreationService:
    """
    Service to orchestrate task creation from natural language input.
    """
    
    def __init__(self, nlp_processor: NaturalLanguageProcessor, task_store: TaskStore):
        self.nlp_processor = nlp_processor
        self.task_store = task_store
    
    def create_task_from_natural_language(self, text: str) -> Task:
        """
        Create a task from natural language input.
        """
        # Process the natural language input
        task_data = self.nlp_processor.process_task_input(text)
        
        # Create the task
        task = Task(
            title=task_data['title'] or task_data['description'][:50] + "..." if len(task_data['description']) > 50 else task_data['description'],
            description=task_data['description'],
            due_date=task_data['due_date'],
            priority=task_data['priority'] or TaskPriority.LOW,
            category=task_data['category'] or ""
        )
        
        # Add the task to the store
        task = self.task_store.add_task(task)
        
        # Create recurrence pattern if specified
        if task_data['recurrence_pattern']:
            self._create_recurrence_pattern(task, task_data['recurrence_pattern'])
        
        # Create reminder settings if specified
        if task_data['reminder_settings']:
            self._create_reminder_settings(task, task_data['reminder_settings'])
        
        return task
    
    def _create_recurrence_pattern(self, task: Task, pattern_data: Dict[str, Any]):
        """
        Create and store a recurrence pattern for the task.
        """
        from datetime import datetime
        
        pattern = RecurrencePattern(
            task_id=task.id,
            pattern_type=pattern_data['pattern_type'],
            interval=pattern_data['interval'],
            days_of_week=pattern_data.get('days_of_week', []),
            day_of_month=pattern_data.get('day_of_month'),
            end_condition=pattern_data.get('end_condition')
        )
        
        # Set the next occurrence based on the pattern
        # This is a simplified implementation - in a real app you'd calculate the next occurrence
        pattern.next_occurrence = datetime.now()
        
        self.task_store.add_recurrence_pattern(pattern)
        
        # Update the task with the recurrence pattern
        task.recurrence_pattern = pattern.to_dict()
        self.task_store.update_task(task)
    
    def _create_reminder_settings(self, task: Task, reminder_data: Dict[str, Any]):
        """
        Create and store reminder settings for the task.
        """
        reminder_settings = ReminderSettings(
            task_id=task.id,
            timing=reminder_data.get('timing'),
            minutes_before=reminder_data.get('minutes_before', 30),
            enabled=True
        )
        
        self.task_store.add_reminder_settings(reminder_settings)
        
        # Update the task with the reminder settings
        task.reminder_settings = reminder_settings.to_dict()
        self.task_store.update_task(task)