"""
Unit tests for the RecurrenceService.
"""
import pytest
from datetime import datetime, timedelta
from src.services.recurrence_service import RecurrenceService
from src.services.task_store import TaskStore
from src.models.task import Task, TaskStatus
from src.models.recurrence import RecurrencePattern, PatternType


class TestRecurrenceService:
    """Test cases for the RecurrenceService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.recurrence_service = RecurrenceService(self.task_store)
    
    def test_generate_next_occurrence_daily(self):
        """Test generating next occurrence for daily pattern."""
        pattern = RecurrencePattern(
            pattern_type=PatternType.DAILY,
            interval=1,
            next_occurrence=datetime.now()
        )
        
        next_date = self.recurrence_service.generate_next_occurrence(pattern)
        
        assert next_date is not None
        # Should be approximately 1 day later
        expected_date = pattern.next_occurrence + timedelta(days=pattern.interval)
        assert abs((next_date - expected_date).total_seconds()) < 60  # Within 1 minute tolerance
    
    def test_handle_completed_recurring_task(self):
        """Test handling a completed recurring task."""
        # Create a recurring task
        task = Task(
            title="Daily Task",
            description="A task that repeats daily",
            due_date=datetime.now(),
            recurrence_pattern={
                "id": "test-pattern-id",
                "pattern_type": PatternType.DAILY,
                "interval": 1
            }
        )
        
        # Add task to store
        task = self.task_store.add_task(task)
        
        # Create and add a recurrence pattern
        pattern = RecurrencePattern(
            id="test-pattern-id",
            task_id=task.id,
            pattern_type=PatternType.DAILY,
            interval=1,
            next_occurrence=datetime.now() + timedelta(days=1)
        )
        self.task_store.add_recurrence_pattern(pattern)
        
        # Complete the task
        task.complete()
        self.task_store.update_task(task)
        
        # Handle the completed recurring task
        new_task = self.recurrence_service.handle_completed_recurring_task(task)
        
        assert new_task is not None
        assert new_task.title == task.title
        assert new_task.status == TaskStatus.PENDING
        assert new_task.due_date > task.due_date