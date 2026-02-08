"""
Integration tests for the complete AI Task Manager workflow.
"""
import pytest
from datetime import datetime, timedelta
from src.main import main
from src.cli.interface import CLIInterface
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.task_store import TaskStore
from src.services.recurrence_service import RecurrenceService
from src.services.notification_service import NotificationService
from src.services.priority_detection import PriorityDetectionService
from src.services.category_detection import CategoryDetectionService


class TestCompleteWorkflow:
    """Integration tests for the complete AI Task Manager workflow."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
        self.recurrence_service = RecurrenceService(self.task_store)
        self.notification_service = NotificationService(self.task_store)
        self.priority_service = PriorityDetectionService()
        self.category_service = CategoryDetectionService()
        
        # Create a CLI interface for testing
        self.cli = CLIInterface()
        # Override the task store in the CLI to use our test store
        self.cli.task_store = self.task_store
        self.cli.nlp_processor = self.nlp_processor
        self.cli.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
    
    def test_complete_ai_task_manager_workflow(self):
        """Test the complete workflow of the AI Task Manager."""
        # Test creating a task with natural language
        task = self.task_creation_service.create_task_from_natural_language("urgent team meeting tomorrow at 10am")
        
        # Verify the task was created with appropriate properties
        assert task is not None
        assert task.title != ""
        assert task.priority.name == "HIGH"  # Should be detected as high priority
        
        # Verify the task is in the store
        stored_task = self.task_store.get_task(task.id)
        assert stored_task is not None
        
        # Test priority detection
        detected_priority = self.priority_service.detect_priority_from_text(stored_task.description)
        assert detected_priority.name == "HIGH"
        
        # Test category detection
        detected_category = self.category_service.detect_category_from_text(stored_task.description)
        # Could be 'work' or None depending on the specific text
        # Just verify the function works without error
        
        # Test recurrence pattern (if applicable)
        if stored_task.recurrence_pattern:
            # If it's a recurring task, test the recurrence service
            next_task = self.recurrence_service.handle_completed_recurring_task(stored_task)
            # This would create the next occurrence if it's recurring
        
        # Test getting all tasks
        all_tasks = self.task_store.get_all_tasks()
        assert len(all_tasks) >= 1
        
        # Test getting tasks by status
        pending_tasks = self.task_store.get_tasks_by_status(stored_task.status)
        assert len(pending_tasks) >= 1
        
        # Test CLI functionality
        # Capture the output of the list command
        import io
        import sys
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.cli.onecmd("list pending")
            output = captured_output.getvalue()
            assert stored_task.title in output
        finally:
            sys.stdout = original_stdout