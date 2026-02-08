"""
Integration tests for the CategoryDetectionService.
"""
import pytest
from src.services.category_detection import CategoryDetectionService
from src.services.task_store import TaskStore
from src.models.task import Task


class TestCategoryDetectionServiceIntegration:
    """Integration tests for the CategoryDetectionService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.category_service = CategoryDetectionService()
    
    def test_category_detection_and_application_workflow(self):
        """Test the full workflow of detecting and applying category to a task."""
        # Create a task with work-related keywords
        task = Task(
            title="Team Meeting",
            description="Attend the weekly team meeting and prepare the status report"
        )
        
        # Add task to store
        task = self.task_store.add_task(task)
        
        # Verify initial category is empty
        assert task.category == ""
        
        # Detect category from the task
        detected_category = self.category_service.detect_category_from_text(task.description)
        assert detected_category == 'work'
        
        # Suggest category for the task
        suggested_category = self.category_service.suggest_category(task)
        assert suggested_category == 'work'
        
        # Apply category suggestion to the task
        updated_task = self.category_service.apply_category_suggestion(task)
        
        # Verify the task category was updated
        assert updated_task.category == 'work'
        
        # Verify the updated task is reflected in the store
        stored_task = self.task_store.get_task(task.id)
        # Note: apply_category_suggestion returns a new object, doesn't update the store automatically
        # So we need to update the store manually
        self.task_store.update_task(updated_task)
        
        # Retrieve and verify
        stored_task = self.task_store.get_task(task.id)
        assert stored_task.category == 'work'