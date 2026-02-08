"""
Integration tests for the RecurrenceService.
"""
import pytest
from datetime import datetime, timedelta
from src.services.recurrence_service import RecurrenceService
from src.services.task_store import TaskStore
from src.models.task import Task, TaskStatus
from src.models.recurrence import RecurrencePattern, PatternType


class TestRecurrenceServiceIntegration:
    """Integration tests for the RecurrenceService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.recurrence_service = RecurrenceService(self.task_store)
    
    def test_full_recurring_task_workflow(self):
        """Test the full workflow of creating, completing, and generating next occurrence of a recurring task."""
        # Create a recurring task
        task = Task(
            title="Daily Exercise",
            description="Do morning exercise routine",
            due_date=datetime.now() + timedelta(minutes=1),  # Due in 1 minute
            recurrence_pattern={
                "id": "daily-exercise-pattern",
                "pattern_type": PatternType.DAILY,
                "interval": 1
            }
        )
        
        # Add task to store
        task = self.task_store.add_task(task)
        
        # Create and add a recurrence pattern
        pattern = RecurrencePattern(
            id="daily-exercise-pattern",
            task_id=task.id,
            pattern_type=PatternType.DAILY,
            interval=1,
            next_occurrence=datetime.now() + timedelta(days=1)  # Next occurrence in 1 day
        )
        self.task_store.add_recurrence_pattern(pattern)
        
        # Verify the task exists in the store
        stored_task = self.task_store.get_task(task.id)
        assert stored_task is not None
        assert stored_task.title == "Daily Exercise"
        
        # Complete the task
        stored_task.complete()
        self.task_store.update_task(stored_task)
        
        # Verify the task is now completed
        updated_task = self.task_store.get_task(task.id)
        assert updated_task.status == TaskStatus.COMPLETED
        
        # Handle the completed recurring task to generate the next occurrence
        next_task = self.recurrence_service.handle_completed_recurring_task(updated_task)
        
        # Verify the next occurrence was created
        assert next_task is not None
        assert next_task.title == "Daily Exercise"
        assert next_task.status == TaskStatus.PENDING
        assert next_task.due_date > updated_task.due_date
        
        # Verify the new task is in the store
        new_stored_task = self.task_store.get_task(next_task.id)
        assert new_stored_task is not None
        assert new_stored_task.title == "Daily Exercise"
        assert new_stored_task.status == TaskStatus.PENDING