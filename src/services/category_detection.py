"""
CategoryDetectionService for detecting and suggesting task categories.
"""
from typing import Dict, List, Optional
from src.models.task import Task


class CategoryDetectionService:
    """
    Service for detecting task categories based on keywords and content.
    """
    
    def __init__(self):
        # Define category keywords
        self.category_keywords = {
            'work': [
                'work', 'office', 'job', 'kaam', 'dafa', 'meeting', 'report', 
                'presentation', 'project', 'client', 'colleague', 'boss', 
                'team', 'assignment', 'task', 'duty', 'responsibility'
            ],
            'study': [
                'study', 'book', 'exam', 'course', 'padhai', 'class', 
                'lecture', 'homework', 'assignment', 'research', 'thesis', 
                'paper', 'study group', 'library', 'education', 'learning'
            ],
            'personal': [
                'personal', 'family', 'ghar', 'khud', 'home', 'household', 
                'grocery', 'shopping', 'appointment', 'personal care', 
                'self-care', 'hobby', 'interest', 'friend', 'relative'
            ],
            'health': [
                'health', 'exercise', 'gym', 'doctor', 'hospital', 'meditation',
                'wellness', 'fitness', 'diet', 'nutrition', 'medical', 
                'therapy', 'pharmacy', 'checkup', 'medicine', 'treatment'
            ],
            'finance': [
                'finance', 'bill', 'payment', 'money', 'paisa', 'budget', 
                'expense', 'income', 'tax', 'investment', 'bank', 'account', 
                'loan', 'insurance', 'financial', 'expense report'
            ]
        }
    
    def detect_category_from_text(self, text: str) -> Optional[str]:
        """
        Detect category based on keywords in the text.
        """
        text_lower = text.lower()
        
        # Count keyword matches for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return the category with the highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return None
    
    def suggest_category(self, task: Task) -> Optional[str]:
        """
        Suggest a category for a task based on its content.
        """
        # Combine title and description for better detection
        content = f"{task.title} {task.description}".lower()
        
        return self.detect_category_from_text(content)
    
    def apply_category_suggestion(self, task: Task) -> Task:
        """
        Apply a category suggestion to a task if it doesn't already have a category.
        """
        if not task.category:  # Only suggest if no category is set
            suggested_category = self.suggest_category(task)
            if suggested_category:
                task.category = suggested_category
        
        return task