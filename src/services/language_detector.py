"""
LanguageDetector service using langdetect library.
"""
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from typing import Dict, List, Tuple
import re


class LanguageDetector:
    """
    Service for detecting language segments in mixed text.
    """
    
    def __init__(self):
        # Define language codes for Urdu and English
        self.urdu_code = 'ur'
        self.english_code = 'en'
    
    def detect_language(self, text: str) -> str:
        """
        Detect the primary language of the text.
        """
        try:
            return detect(text)
        except LangDetectException:
            # If detection fails, default to English
            return self.english_code
    
    def detect_language_proba(self, text: str) -> List[Tuple[str, float]]:
        """
        Detect language probabilities for the text.
        """
        try:
            langs = detect_langs(text)
            return [(lang.lang, lang.prob) for lang in langs]
        except LangDetectException:
            # If detection fails, return English with low probability
            return [(self.english_code, 0.1)]
    
    def segment_mixed_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Segment mixed text into language-specific segments.
        Returns a list of tuples (segment_text, language_code).
        """
        # This is a simplified implementation
        # In a production system, you'd want more sophisticated segmentation
        
        # Split text by spaces but preserve punctuation
        words = re.findall(r'\S+|\s+', text)
        
        segments = []
        current_segment = ""
        current_lang = None
        
        for word in words:
            if word.strip():  # Non-whitespace
                word_lang = self.detect_language(word.strip())
                
                if current_lang is None:
                    current_lang = word_lang
                    current_segment = word
                elif current_lang == word_lang:
                    current_segment += word
                else:
                    # Language changed, save current segment and start new one
                    if current_segment.strip():
                        segments.append((current_segment.strip(), current_lang))
                    current_segment = word
                    current_lang = word_lang
            else:  # Whitespace
                current_segment += word
        
        # Add the last segment
        if current_segment.strip():
            segments.append((current_segment.strip(), current_lang or self.english_code))
        
        return segments
    
    def is_urdu_english_mixed(self, text: str) -> bool:
        """
        Check if the text contains both Urdu and English segments.
        """
        languages_found = set()
        
        # Detect language for the whole text
        try:
            primary_lang = detect(text)
            languages_found.add(primary_lang)
        except LangDetectException:
            pass
        
        # If we have both Urdu and English, return True
        return self.urdu_code in languages_found and self.english_code in languages_found