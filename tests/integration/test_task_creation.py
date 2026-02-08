"""
Integration tests for the TaskCreationService.
"""
import pytest
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.task_store import TaskStore


class TestTaskCreationService:
    """Integration tests for the TaskCreationService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(
            nlp_processor=self.nlp_processor,
            task_store=self.task_store
        )
    
    def test_create_task_from_natural_language(self):
        """Test creating a task from natural language input."""
        text = "buy groceries tomorrow"
        
        task = self.task_creation_service.create_task_from_natural_language(text)
        
        # Verify the task was created
        assert task is not None
        assert task.title != ""
        assert task.description == text
        
        # Verify the task is in the store
        retrieved_task = self.task_store.get_task(task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
    
    def test_create_task_with_priority_keyword(self):
        """Test creating a task with priority keywords."""
        text = "urgent buy groceries tomorrow"
        
        task = self.task_creation_service.create_task_from_natural_language(text)
        
        # Verify the task has high priority
        assert task.priority.name == "HIGH"
    
    def test_create_task_with_category_keyword(self):
        """Test creating a task with category keywords."""
        text = "buy office supplies next week"
        
        task = self.task_creation_service.create_task_from_natural_language(text)
        
        # Verify the task has work category
        assert task.category == "work"