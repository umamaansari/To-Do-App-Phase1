"""
NaturalLanguageProcessor service using spaCy for Urdu-English code-switching.
"""
import re
from typing import Dict, Any, Optional
from src.services.date_time_parser import DateTimeParser
from src.services.language_detector import LanguageDetector
from src.models.task import Task, TaskPriority
from src.models.recurrence import RecurrencePattern, PatternType, EndCondition, EndConditionType
from src.models.reminder_settings import ReminderSettings, ReminderMethod, ReminderTiming


class NaturalLanguageProcessor:
    """
    Service for processing natural language input to extract task information.
    """
    
    def __init__(self):
        self.datetime_parser = DateTimeParser()
        self.language_detector = LanguageDetector()
        
        # Define priority keywords
        self.high_priority_keywords = [
            'urgent', 'asap', 'immediately', 'zaroori', 'jis', 'jaldi', 'important'
        ]
        self.medium_priority_keywords = [
            'soon', 'this week', 'this month', 'normal', 'medium'
        ]
        
        # Define category keywords
        self.category_keywords = {
            'work': ['work', 'office', 'job', 'kaam', 'dafa'],
            'study': ['study', 'book', 'exam', 'course', 'padhai', 'class'],
            'personal': ['personal', 'family', 'ghar', 'khud'],
            'health': ['health', 'exercise', 'gym', 'doctor', 'hospital', 'meditation'],
            'finance': ['finance', 'bill', 'payment', 'money', 'paisa', 'budget']
        }
    
    def process_task_input(self, text: str) -> Dict[str, Any]:
        """
        Process natural language input and extract task information.
        """
        result = {
            'title': '',
            'description': text,
            'due_date': None,
            'recurrence_pattern': None,
            'reminder_settings': None,
            'priority': None,
            'category': None
        }
        
        # Extract task title (basic implementation)
        result['title'] = self._extract_title(text)
        
        # Extract date/time
        result['due_date'] = self.datetime_parser.parse_datetime(text)
        
        # Extract recurrence pattern
        result['recurrence_pattern'] = self._extract_recurrence_pattern(text)
        
        # Extract reminder preferences
        result['reminder_settings'] = self._extract_reminder_settings(text)
        
        # Extract priority
        result['priority'] = self._determine_priority(text)
        
        # Extract category
        result['category'] = self._determine_category(text)
        
        return result
    
    def _extract_title(self, text: str) -> str:
        """
        Extract the task title from the input text.
        """
        # Remove common phrases that indicate recurrence or timing
        cleaned_text = re.sub(r'\b(har|roz|kal|aaj|iss hafte|agla hafte|iss mah|agle mah)\b', '', text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\b(daily|weekly|monthly|tomorrow|today|this week|next week|this month|next month)\b', '', cleaned_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\b(subah|dopahar|sham|morning|afternoon|evening|night)\b', '', cleaned_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\d+\s*(am|pm|baje)?', '', cleaned_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\d+\s*(day|days|week|weeks|month|months|year|years)', '', cleaned_text, flags=re.IGNORECASE)
        
        # Extract the main task content
        # This is a simplified approach - in a real app you'd want more sophisticated NLP
        title_words = []
        for word in cleaned_text.split():
            # Skip common verbs and articles
            if word.lower() not in ['ko', 'pe', 'for', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at']:
                title_words.append(word)
        
        return ' '.join(title_words).strip()
    
    def _extract_recurrence_pattern(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract recurrence pattern from the input text.
        """
        pattern_info = self.datetime_parser.parse_recurring_pattern(text)
        
        if pattern_info:
            # Convert to the format expected by RecurrencePattern
            pattern_type = PatternType.DAILY
            if pattern_info['type'] == 'weekly':
                pattern_type = PatternType.WEEKLY
            elif pattern_info['type'] == 'monthly':
                pattern_type = PatternType.MONTHLY
            elif pattern_info['type'] == 'yearly':
                pattern_type = PatternType.YEARLY
            elif pattern_info['type'] == 'custom':
                pattern_type = PatternType.CUSTOM
            
            return {
                'pattern_type': pattern_type,
                'interval': pattern_info['interval'],
                'days_of_week': pattern_info['days_of_week'],
                'day_of_month': pattern_info['day_of_month'],
                'end_condition': None  # Would need to parse end conditions separately
            }
        
        return None
    
    def _extract_reminder_settings(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract reminder preferences from the input text.
        """
        # Look for common reminder expressions
        if 'remind' in text.lower() or 'yaad' in text.lower():
            # Check for timing preferences
            if '1 din pehle' in text or '1 day before' in text:
                return {
                    'timing': ReminderTiming.BEFORE_DUE,
                    'minutes_before': 24 * 60  # 1 day in minutes
                }
            elif '30 min pehle' in text or '30 minutes before' in text:
                return {
                    'timing': ReminderTiming.BEFORE_DUE,
                    'minutes_before': 30
                }
            elif '2 hours pehle' in text or '2 hours before' in text:
                return {
                    'timing': ReminderTiming.BEFORE_DUE,
                    'minutes_before': 2 * 60  # 2 hours in minutes
                }
            elif 'morning mein yaad' in text or 'remind in morning' in text:
                # This would require more complex handling
                return {
                    'timing': ReminderTiming.CUSTOM,
                    'minutes_before': 30
                }
        
        return None
    
    def _determine_priority(self, text: str) -> TaskPriority:
        """
        Determine task priority based on keywords in the text.
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
    
    def _determine_category(self, text: str) -> Optional[str]:
        """
        Determine task category based on keywords in the text.
        """
        text_lower = text.lower()
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return None