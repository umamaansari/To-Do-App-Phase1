"""
DateTimeParser service using parsedatetime and pytz for timezone handling.
"""
import parsedatetime
from datetime import datetime, timedelta
import pytz
from typing import Optional, Tuple
import re


class DateTimeParser:
    """
    Service for parsing date/time expressions using parsedatetime and pytz.
    """
    
    def __init__(self, timezone_str: str = "Asia/Karachi"):
        self.cal = parsedatetime.Calendar()
        self.timezone = pytz.timezone(timezone_str)
    
    def parse_datetime(self, text: str) -> Optional[datetime]:
        """
        Parse a natural language date/time expression and return a timezone-aware datetime.
        """
        # Handle some common Urdu expressions by converting to English equivalents
        text = self._convert_urdu_to_english_numbers(text)
        text = self._normalize_urdu_expressions(text)
        
        # Parse the date/time
        time_struct, parse_status = self.cal.parse(text)
        
        if parse_status != 0:  # 0 means parsing failed
            dt = datetime(*time_struct[:6])
            # Convert to timezone-aware datetime
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            else:
                dt = dt.astimezone(self.timezone)
            return dt
        
        return None
    
    def _convert_urdu_to_english_numbers(self, text: str) -> str:
        """
        Convert Urdu numerals to English numerals in the text.
        """
        urdu_numerals = {
            '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
            '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
        }
        
        for urdu_num, eng_num in urdu_numerals.items():
            text = text.replace(urdu_num, eng_num)
        
        return text
    
    def _normalize_urdu_expressions(self, text: str) -> str:
        """
        Normalize common Urdu expressions to English equivalents that parsedatetime can understand.
        """
        # Dictionary mapping common Urdu expressions to English
        urdu_to_eng = {
            'roz': 'daily',
            'har roz': 'daily',
            'kal': 'tomorrow',
            'kal subah': 'tomorrow morning',
            'kal sham': 'tomorrow evening',
            'kal dopahar': 'tomorrow afternoon',
            'aaj': 'today',
            'aaj sham': 'today evening',
            'aaj dopahar': 'today afternoon',
            'aaj subah': 'today morning',
            'kal raat': 'tomorrow night',
            'iss hafte': 'this week',
            'agla hafte': 'next week',
            'iss mah': 'this month',
            'agle mah': 'next month',
            'iss saal': 'this year',
            'agle saal': 'next year',
            'din': 'day',
            'hafte': 'week',
            'mah': 'month',
            'saal': 'year',
            'subah': 'morning',
            'dopahar': 'afternoon',
            'sham': 'evening',
            'raat': 'night',
            'baje': "o'clock",
            'pehle': 'before',
            'baad': 'after'
        }
        
        # Sort keys by length in descending order to avoid partial replacements
        sorted_keys = sorted(urdu_to_eng.keys(), key=len, reverse=True)
        
        for key in sorted_keys:
            text = re.sub(r'\b' + re.escape(key) + r'\b', urdu_to_eng[key], text, flags=re.IGNORECASE)
        
        return text
    
    def parse_recurring_pattern(self, text: str) -> Optional[dict]:
        """
        Parse recurring pattern from text and return a dict with pattern details.
        """
        # This is a simplified implementation - in a real app, you'd want more sophisticated parsing
        text_lower = text.lower()
        
        pattern_info = {
            'type': 'daily',  # default
            'interval': 1,
            'days_of_week': [],
            'day_of_month': None
        }
        
        # Check for daily patterns
        if 'roz' in text_lower or 'daily' in text_lower or 'har roz' in text_lower:
            pattern_info['type'] = 'daily'
            pattern_info['interval'] = 1
        elif 'har' in text_lower and ('din' in text_lower or 'day' in text_lower):
            # Handle patterns like "har 2 din" (every 2 days)
            match = re.search(r'har\s+(\d+)\s+(din|days?)', text_lower)
            if match:
                pattern_info['type'] = 'daily'
                pattern_info['interval'] = int(match.group(1))
        
        # Check for weekly patterns
        elif 'hafte' in text_lower or 'week' in text_lower:
            pattern_info['type'] = 'weekly'
            # Check for specific days
            days_map = {
                'monday': 0, 'mon': 0, 'somvar': 0, 'som': 0,
                'tuesday': 1, 'tue': 1, 'mangal': 1, 'mang': 1,
                'wednesday': 2, 'wed': 2, 'budh': 2, 'budhvar': 2,
                'thursday': 3, 'thu': 3, 'guru': 3, 'guruvar': 3,
                'friday': 4, 'fri': 4, 'shukr': 4, 'shukrvar': 4,
                'saturday': 5, 'sat': 5, 'shanivar': 5, 'shan': 5,
                'sunday': 6, 'sun': 6, 'itwar': 6, 'ivr': 6
            }
            
            for day, day_idx in days_map.items():
                if day in text_lower:
                    pattern_info['days_of_week'] = [day_idx]
                    break
            
            # Handle patterns like "har 2 hafte" (every 2 weeks)
            match = re.search(r'har\s+(\d+)\s+(hafte|weeks?)', text_lower)
            if match:
                pattern_info['interval'] = int(match.group(1))
        
        # Check for monthly patterns
        elif 'mah' in text_lower or 'month' in text_lower:
            pattern_info['type'] = 'monthly'
            # Handle patterns like "har mah 5 tarikh ko" (on 5th of every month)
            match = re.search(r'(?:har mah|monthly)\s*(\d+)', text_lower)
            if match:
                pattern_info['day_of_month'] = int(match.group(1))
        
        # Check for yearly patterns
        elif 'saal' in text_lower or 'year' in text_lower:
            pattern_info['type'] = 'yearly'
        
        return pattern_info