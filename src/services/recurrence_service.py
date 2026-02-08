"""
RecurrenceService for managing recurring tasks.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from src.models.task import Task, TaskStatus
from src.models.recurrence import RecurrencePattern, PatternType, EndConditionType
from src.services.task_store import TaskStore


class RecurrenceService:
    """
    Service for managing recurring tasks and their patterns.
    """
    
    def __init__(self, task_store: TaskStore):
        self.task_store = task_store
    
    def generate_next_occurrence(self, pattern: RecurrencePattern) -> Optional[datetime]:
        """
        Generate the next occurrence date based on the recurrence pattern.
        """
        # This is a simplified implementation
        # In a real app, you'd use dateutil.rrule for complex recurrence patterns
        
        if not pattern.next_occurrence:
            # If there's no next occurrence set, we can't generate the next one
            return None
        
        current_date = pattern.next_occurrence
        
        if pattern.pattern_type == PatternType.DAILY:
            next_date = current_date + timedelta(days=pattern.interval)
        elif pattern.pattern_type == PatternType.WEEKLY:
            next_date = current_date + timedelta(weeks=pattern.interval)
        elif pattern.pattern_type == PatternType.MONTHLY:
            # Simplified monthly calculation (adding ~30 days)
            next_date = current_date + timedelta(days=30 * pattern.interval)
        elif pattern.pattern_type == PatternType.YEARLY:
            # Simplified yearly calculation (adding 365 days)
            next_date = current_date + timedelta(days=365 * pattern.interval)
        else:
            # For custom patterns, we'd need more complex logic
            return None
        
        # Check if this date is in the exceptions list
        while next_date.date() in [exc_date for exc_date in pattern.exceptions]:
            if pattern.pattern_type == PatternType.DAILY:
                next_date = next_date + timedelta(days=pattern.interval)
            elif pattern.pattern_type == PatternType.WEEKLY:
                next_date = next_date + timedelta(weeks=pattern.interval)
            elif pattern.pattern_type == PatternType.MONTHLY:
                next_date = next_date + timedelta(days=30 * pattern.interval)
            elif pattern.pattern_type == PatternType.YEARLY:
                next_date = next_date + timedelta(days=365 * pattern.interval)
        
        # Check end condition
        if pattern.end_condition:
            if pattern.end_condition.type == EndConditionType.ON_DATE:
                if next_date.date() > pattern.end_condition.date:
                    return None
            elif pattern.end_condition.type == EndConditionType.AFTER_OCCURRENCES:
                # This would require tracking the number of occurrences
                # Simplified implementation ignores this for now
                pass
        
        return next_date
    
    def handle_completed_recurring_task(self, task: Task) -> Optional[Task]:
        """
        Handle a completed recurring task by creating the next occurrence.
        """
        if not task.recurrence_pattern:
            return None
        
        # Get the recurrence pattern
        pattern = self.task_store.get_recurrence_pattern(task.recurrence_pattern.get('id', ''))
        if not pattern:
            return None
        
        # Generate the next occurrence date
        next_date = self.generate_next_occurrence(pattern)
        if not next_date:
            # No more occurrences, possibly due to end condition
            return None
        
        # Create a new task with the same properties but updated due date
        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=next_date,
            status=TaskStatus.PENDING,
            priority=task.priority,
            category=task.category,
            notes=task.notes,
            recurrence_pattern=task.recurrence_pattern,
            reminder_settings=task.reminder_settings,
            estimated_duration=task.estimated_duration
        )
        
        # Add the new task to the store
        new_task = self.task_store.add_task(new_task)
        
        # Update the pattern's next occurrence
        pattern.next_occurrence = next_date
        self.task_store.add_recurrence_pattern(pattern)
        
        return new_task
    
    def skip_recurring_task_instance(self, task: Task) -> bool:
        """
        Skip a recurring task instance and schedule the next one.
        """
        if not task.recurrence_pattern:
            return False
        
        # Get the recurrence pattern
        pattern = self.task_store.get_recurrence_pattern(task.recurrence_pattern.get('id', ''))
        if not pattern:
            return False
        
        # Add the current date to exceptions to skip this instance
        pattern.exceptions.append(task.due_date.date() if task.due_date else datetime.now().date())
        
        # Generate the next occurrence date
        next_date = self.generate_next_occurrence(pattern)
        if not next_date:
            return False
        
        # Create a new task with the same properties but updated due date
        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=next_date,
            status=TaskStatus.PENDING,
            priority=task.priority,
            category=task.category,
            notes=task.notes,
            recurrence_pattern=task.recurrence_pattern,
            reminder_settings=task.reminder_settings,
            estimated_duration=task.estimated_duration
        )
        
        # Add the new task to the store
        new_task = self.task_store.add_task(new_task)
        
        # Update the pattern's next occurrence
        pattern.next_occurrence = next_date
        self.task_store.add_recurrence_pattern(pattern)
        
        # Mark the current task as skipped
        task.skip()
        self.task_store.update_task(task)
        
        return True
    
    def get_upcoming_recurring_tasks(self, days_ahead: int = 7) -> List[Task]:
        """
        Get recurring tasks that will be due in the next specified number of days.
        """
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        upcoming_tasks = []
        all_tasks = self.task_store.get_all_tasks()
        
        for task in all_tasks:
            if task.recurrence_pattern and task.status == TaskStatus.PENDING:
                pattern = self.task_store.get_recurrence_pattern(task.recurrence_pattern.get('id', ''))
                if pattern and pattern.next_occurrence and pattern.next_occurrence <= end_date:
                    upcoming_tasks.append(task)
        
        return upcoming_tasks