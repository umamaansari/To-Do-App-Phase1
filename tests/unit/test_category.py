"""
Unit tests for the CategoryDetectionService.
"""
import pytest
from src.services.category_detection import CategoryDetectionService
from src.models.task import Task


class TestCategoryDetectionService:
    """Test cases for the CategoryDetectionService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.service = CategoryDetectionService()
    
    def test_detect_work_category_from_text(self):
        """Test detecting work category from text."""
        text = "Prepare presentation for the client meeting tomorrow"
        category = self.service.detect_category_from_text(text)
        
        assert category == 'work'
    
    def test_detect_study_category_from_text(self):
        """Test detecting study category from text."""
        text = "Study for the mathematics exam next week"
        category = self.service.detect_category_from_text(text)
        
        assert category == 'study'
    
    def test_detect_health_category_from_text(self):
        """Test detecting health category from text."""
        text = "Go to the doctor for a checkup and visit the gym"
        category = self.service.detect_category_from_text(text)
        
        assert category == 'health'
    
    def test_detect_finance_category_from_text(self):
        """Test detecting finance category from text."""
        text = "Pay the electricity bill and review monthly expenses"
        category = self.service.detect_category_from_text(text)
        
        assert category == 'finance'
    
    def test_suggest_category_for_task(self):
        """Test suggesting category for a task."""
        task = Task(
            title="Team meeting",
            description="Attend the weekly team meeting and prepare report"
        )
        
        suggested_category = self.service.suggest_category(task)
        
        assert suggested_category == 'work'
    
    def test_apply_category_suggestion(self):
        """Test applying category suggestion to a task."""
        task = Task(
            title="Doctor appointment",
            description="Visit the doctor for annual checkup"
        )
        
        updated_task = self.service.apply_category_suggestion(task)
        
        assert updated_task.category == 'health'