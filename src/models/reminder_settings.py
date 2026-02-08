"""
ReminderSettings model configuring when and how the user is reminded about a task.
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass, field


class ReminderMethod(Enum):
    NOTIFICATION = "notification"
    EMAIL = "email"
    SMS = "sms"


class ReminderTiming(Enum):
    AT_DUE_TIME = "at_due_time"
    BEFORE_DUE = "before_due"
    CUSTOM = "custom"


@dataclass
class ReminderSettings:
    """
    Configures when and how the user is reminded about a task.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    method: ReminderMethod = ReminderMethod.NOTIFICATION
    timing: ReminderTiming = ReminderTiming.BEFORE_DUE
    minutes_before: Optional[int] = 30  # Minutes before due time (for "before_due" and "custom")
    enabled: bool = True  # Whether reminders are active for this task
    last_reminder_sent: Optional[datetime] = None

    def __post_init__(self):
        """Validate the reminder settings after initialization."""
        if not self.task_id:
            raise ValueError("Task ID must be provided for reminder settings")
        
        if self.timing in [ReminderTiming.BEFORE_DUE, ReminderTiming.CUSTOM] and \
           (self.minutes_before is None or self.minutes_before <= 0):
            raise ValueError("Minutes before must be positive for 'before_due' and 'custom' timing")

    def to_dict(self):
        """Convert the reminder settings to a dictionary representation."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "method": self.method.value,
            "timing": self.timing.value,
            "minutes_before": self.minutes_before,
            "enabled": self.enabled,
            "last_reminder_sent": self.last_reminder_sent.isoformat() if self.last_reminder_sent else None
        }