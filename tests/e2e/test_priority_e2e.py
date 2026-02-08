"""
End-to-end tests for the priority detection functionality.
"""
import pytest
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.priority_detection import PriorityDetectionService
from src.services.task_store import TaskStore
from src.models.task import TaskPriority


class TestPriorityEndToEnd:
    """End-to-end tests for priority detection functionality."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
        self.priority_service = PriorityDetectionService()
    
    def test_end_to_end_priority_detection_workflow(self):
        """Test the complete workflow of creating a task and detecting its priority."""
        # Create a task with high priority indicators using natural language
        task = self.task_creation_service.create_task_from_natural_language("urgent meeting with boss asap")
        
        # Verify the task was created
        assert task is not None
        assert task.title != "" or task.description != ""
        
        # Verify the task is in the store
        stored_task = self.task_store.get_task(task.id)
        assert stored_task is not None
        
        # Detect priority from the stored task
        detected_priority = self.priority_service.detect_priority_from_text(stored_task.description)
        assert detected_priority == TaskPriority.HIGH
        
        # Apply priority suggestion to the task
        updated_task = self.priority_service.apply_priority_suggestion(stored_task)
        
        # Verify the priority was applied
        assert updated_task.priority == TaskPriority.HIGH
        
        # Update the task in the store
        self.task_store.update_task(updated_task)
        
        # Retrieve and verify
        final_task = self.task_store.get_task(task.id)
        assert final_task.priority == TaskPriority.HIGH