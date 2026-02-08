"""
End-to-end tests for the recurring task functionality.
"""
import pytest
from datetime import datetime, timedelta
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.recurrence_service import RecurrenceService
from src.services.task_store import TaskStore


class TestRecurringTaskEndToEnd:
    """End-to-end tests for recurring task functionality."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
        self.recurrence_service = RecurrenceService(self.task_store)
    
    def test_end_to_end_recurring_task_workflow(self):
        """Test the complete workflow of creating, completing, and generating next occurrence of a recurring task."""
        # Create a recurring task using natural language
        task = self.task_creation_service.create_task_from_natural_language("roz subah gym")
        
        # Verify the task was created with appropriate properties
        assert task.title.lower() == "gym" or "gym" in task.title.lower()
        assert task.recurrence_pattern is not None
        assert task.status.name == "PENDING"
        
        # Verify the task is in the store
        stored_task = self.task_store.get_task(task.id)
        assert stored_task is not None
        
        # Complete the recurring task
        stored_task.complete()
        self.task_store.update_task(stored_task)
        
        # Verify the task is now completed
        completed_task = self.task_store.get_task(task.id)
        assert completed_task.status.name == "COMPLETED"
        
        # Handle the completed recurring task to generate the next occurrence
        next_task = self.recurrence_service.handle_completed_recurring_task(completed_task)
        
        # Verify the next occurrence was created
        assert next_task is not None
        assert next_task.title == stored_task.title
        assert next_task.status.name == "PENDING"
        assert next_task.due_date > stored_task.due_date
        
        # Verify the new task is in the store
        new_stored_task = self.task_store.get_task(next_task.id)
        assert new_stored_task is not None
        assert new_stored_task.title == stored_task.title
        assert new_stored_task.status.name == "PENDING"