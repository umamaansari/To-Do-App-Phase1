"""
PriorityDetectionService for detecting and suggesting task priorities.
"""
from typing import Dict, List
from src.models.task import Task, TaskPriority


class PriorityDetectionService:
    """
    Service for detecting task priority based on keywords and other factors.
    """
    
    def __init__(self):
        # Define priority keywords
        self.high_priority_keywords = [
            'urgent', 'asap', 'immediately', 'emergency', 'critical', 'crucial',
            'deadline', 'zaroori', 'jis', 'jaldi', 'important', 'priority',
            'urgent!', 'as soon as possible', 'right now', 'today'
        ]
        
        self.medium_priority_keywords = [
            'soon', 'this week', 'this month', 'normal', 'medium',
            'standard', 'routine', 'regular', 'within days', 'next'
        ]
    
    def detect_priority_from_text(self, text: str) -> TaskPriority:
        """
        Detect priority level based on keywords in the text.
        """
        text_lower = text.lower()
        
        # Check for high priority keywords
        for keyword in self.high_priority_keywords:
            if keyword in text_lower:
                return TaskPriority.HIGH
        
        # Check for medium priority keywords
        for keyword in self.medium_priority_keywords:
            if keyword in text_lower:
                return TaskPriority.MEDIUM
        
        # Default to low priority
        return TaskPriority.LOW
    
    def suggest_priority(self, task: Task) -> TaskPriority:
        """
        Suggest a priority for a task based on its content and other factors.
        """
        # Start with priority detected from the task description
        suggested_priority = self.detect_priority_from_text(task.description or task.title)
        
        # Consider other factors that might influence priority
        # For example, due date proximity could increase priority
        if task.due_date:
            from datetime import datetime
            time_diff = task.due_date - datetime.now()
            
            # If due within 24 hours, increase priority
            if time_diff.total_seconds() < 24 * 3600 and suggested_priority != TaskPriority.HIGH:
                if suggested_priority == TaskPriority.LOW:
                    suggested_priority = TaskPriority.MEDIUM
                # If already medium, keep as medium (don't automatically promote to high)
        
        return suggested_priority
    
    def apply_priority_suggestion(self, task: Task) -> Task:
        """
        Apply a priority suggestion to a task if it doesn't already have a priority.
        """
        if task.priority == TaskPriority.LOW:  # Only suggest if not already set to specific priority
            suggested_priority = self.suggest_priority(task)
            task.priority = suggested_priority
        
        return task