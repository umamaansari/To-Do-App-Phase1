"""
Unit tests for the NaturalLanguageProcessor service.
"""
import pytest
from src.services.nlp_service import NaturalLanguageProcessor


class TestNaturalLanguageProcessor:
    """Test cases for the NaturalLanguageProcessor service."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.processor = NaturalLanguageProcessor()
    
    def test_extract_title_basic(self):
        """Test extracting a basic title from input."""
        text = "roz subah gym"
        result = self.processor._extract_title(text)
        
        # The title extraction is basic, so we expect "gym" to be extracted
        assert "gym" in result.lower()
    
    def test_determine_priority_high(self):
        """Test determining high priority from keywords."""
        text = "urgent meeting with boss"
        priority = self.processor._determine_priority(text)
        
        assert priority.name == "HIGH"
    
    def test_determine_priority_medium(self):
        """Test determining medium priority from keywords."""
        text = "this week project submission"
        priority = self.processor._determine_priority(text)
        
        assert priority.name == "MEDIUM"
    
    def test_determine_priority_low_default(self):
        """Test that low priority is default."""
        text = "regular task"
        priority = self.processor._determine_priority(text)
        
        assert priority.name == "LOW"
    
    def test_determine_category_work(self):
        """Test determining work category from keywords."""
        text = "office meeting tomorrow"
        category = self.processor._determine_category(text)
        
        assert category == "work"
    
    def test_determine_category_study(self):
        """Test determining study category from keywords."""
        text = "study for exams next week"
        category = self.processor._determine_category(text)
        
        assert category == "study"
    
    def test_process_task_input_basic(self):
        """Test processing basic task input."""
        text = "buy groceries tomorrow"
        result = self.processor.process_task_input(text)
        
        assert result['title'] != ''
        assert result['description'] == text
        assert result['priority'] is not None
        assert result['category'] is None  # No category keywords in this text