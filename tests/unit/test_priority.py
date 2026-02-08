"""
Unit tests for the PriorityDetectionService.
"""
import pytest
from src.services.priority_detection import PriorityDetectionService
from src.models.task import Task, TaskPriority


class TestPriorityDetectionService:
    """Test cases for the PriorityDetectionService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.service = PriorityDetectionService()
    
    def test_detect_high_priority_from_text(self):
        """Test detecting high priority from text."""
        text = "This is an urgent task that needs to be done asap!"
        priority = self.service.detect_priority_from_text(text)
        
        assert priority == TaskPriority.HIGH
    
    def test_detect_medium_priority_from_text(self):
        """Test detecting medium priority from text."""
        text = "This task should be done soon or within this week"
        priority = self.service.detect_priority_from_text(text)
        
        assert priority == TaskPriority.MEDIUM
    
    def test_detect_low_priority_from_text(self):
        """Test detecting low priority from text."""
        text = "This is a regular task for later"
        priority = self.service.detect_priority_from_text(text)
        
        assert priority == TaskPriority.LOW
    
    def test_suggest_priority_for_task(self):
        """Test suggesting priority for a task."""
        task = Task(
            title="Complete project proposal",
            description="This is an urgent project proposal that needs to be done asap"
        )
        
        suggested_priority = self.service.suggest_priority(task)
        
        assert suggested_priority == TaskPriority.HIGH
    
    def test_apply_priority_suggestion(self):
        """Test applying priority suggestion to a task."""
        task = Task(
            title="Review documents",
            description="Need to review these documents soon"
        )
        
        updated_task = self.service.apply_priority_suggestion(task)
        
        assert updated_task.priority != TaskPriority.LOW  # Should be upgraded from default