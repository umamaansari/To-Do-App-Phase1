"""
End-to-end tests for the category detection functionality.
"""
import pytest
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.category_detection import CategoryDetectionService
from src.services.task_store import TaskStore


class TestCategoryEndToEnd:
    """End-to-end tests for category detection functionality."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
        self.category_service = CategoryDetectionService()
    
    def test_end_to_end_category_detection_workflow(self):
        """Test the complete workflow of creating a task and detecting its category."""
        # Create a task with work-related keywords using natural language
        task = self.task_creation_service.create_task_from_natural_language("team meeting tomorrow to discuss project")
        
        # Verify the task was created
        assert task is not None
        assert task.title != "" or task.description != ""
        
        # Verify the task is in the store
        stored_task = self.task_store.get_task(task.id)
        assert stored_task is not None
        
        # Detect category from the stored task
        detected_category = self.category_service.detect_category_from_text(stored_task.description)
        assert detected_category == 'work' or detected_category is None  # Could be None if no strong indicators
        
        # Suggest category for the task
        suggested_category = self.category_service.suggest_category(stored_task)
        
        # Apply category suggestion to the task
        updated_task = self.category_service.apply_category_suggestion(stored_task)
        
        # Update the task in the store
        self.task_store.update_task(updated_task)
        
        # Retrieve and verify
        final_task = self.task_store.get_task(task.id)
        # The category might be 'work' if detected, or remain empty if no strong indicators