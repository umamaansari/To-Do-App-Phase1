"""
UserProfile model storing user preferences and persistent data.
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class UserProfile:
    """
    Stores user preferences and persistent data.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timezone: str = "Asia/Karachi"  # Default to Pakistan timezone
    language_preference: str = "urdu-english"  # Preferred language (e.g., "urdu-english")
    notification_preferences: Dict[str, Any] = field(default_factory=dict)  # User's notification settings
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_active: Optional[datetime] = None
    ai_model_preferences: Dict[str, Any] = field(default_factory=dict)  # Preferences for AI behavior and suggestions

    def __post_init__(self):
        """Validate the user profile after initialization."""
        # Note: We're not validating timezone format here to avoid importing pytz in this module
        # Validation would happen at the service level
        
        if self.language_preference not in ["urdu-english", "english", "urdu"]:
            raise ValueError("Language preference must be one of: 'urdu-english', 'english', 'urdu'")

    def update_last_active(self):
        """Update the last active timestamp."""
        self.last_active = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the user profile to a dictionary representation."""
        return {
            "id": self.id,
            "timezone": self.timezone,
            "language_preference": self.language_preference,
            "notification_preferences": self.notification_preferences,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "ai_model_preferences": self.ai_model_preferences
        }