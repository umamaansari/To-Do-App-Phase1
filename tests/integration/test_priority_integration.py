"""
Integration tests for the PriorityDetectionService.
"""
import pytest
from src.services.priority_detection import PriorityDetectionService
from src.services.task_store import TaskStore
from src.models.task import Task, TaskPriority


class TestPriorityDetectionServiceIntegration:
    """Integration tests for the PriorityDetectionService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.priority_service = PriorityDetectionService()
    
    def test_priority_detection_and_application_workflow(self):
        """Test the full workflow of detecting and applying priority to a task."""
        # Create a task with high priority indicators in the description
        task = Task(
            title="Project Deadline",
            description="This is an urgent project that needs to be completed asap today"
        )
        
        # Add task to store
        task = self.task_store.add_task(task)
        
        # Verify initial priority is low (default)
        assert task.priority == TaskPriority.LOW
        
        # Detect priority from the task
        detected_priority = self.priority_service.detect_priority_from_text(task.description)
        assert detected_priority == TaskPriority.HIGH
        
        # Apply priority suggestion to the task
        updated_task = self.priority_service.apply_priority_suggestion(task)
        
        # Verify the task priority was updated
        assert updated_task.priority == TaskPriority.HIGH
        
        # Verify the updated task is reflected in the store
        stored_task = self.task_store.get_task(task.id)
        # Note: apply_priority_suggestion returns a new object, doesn't update the store automatically
        # So we need to update the store manually
        self.task_store.update_task(updated_task)
        
        # Retrieve and verify
        stored_task = self.task_store.get_task(task.id)
        assert stored_task.priority == TaskPriority.HIGH