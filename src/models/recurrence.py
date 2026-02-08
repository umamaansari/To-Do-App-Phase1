"""
RecurrencePattern model defining how a task repeats over time.
"""
import uuid
from datetime import datetime, date
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


class PatternType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class EndConditionType(Enum):
    AFTER_OCCURRENCES = "after_occurrences"
    ON_DATE = "on_date"
    NEVER = "never"


@dataclass
class EndCondition:
    """
    Specifies when a recurring task should stop repeating.
    """
    type: EndConditionType
    count: Optional[int] = None  # Number of occurrences (for "after_occurrences")
    date: Optional[date] = None  # Specific end date (for "on_date")

    def __post_init__(self):
        """Validate the end condition after initialization."""
        if self.type == EndConditionType.AFTER_OCCURRENCES and (self.count is None or self.count <= 0):
            raise ValueError("Count must be positive for 'after_occurrences' end condition")
        
        if self.type == EndConditionType.ON_DATE and self.date is None:
            raise ValueError("Date must be provided for 'on_date' end condition")


@dataclass
class RecurrencePattern:
    """
    Defines how a task repeats over time.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    pattern_type: PatternType = PatternType.DAILY
    interval: int = 1  # How often the pattern repeats (e.g., every 2 weeks)
    days_of_week: List[int] = field(default_factory=list)  # Days of week for weekly patterns (0=Monday, 6=Sunday)
    day_of_month: Optional[int] = None  # Day of month for monthly patterns (1-31)
    exceptions: List[date] = field(default_factory=list)  # Specific dates to skip (list of date strings)
    end_condition: Optional[EndCondition] = None
    next_occurrence: Optional[datetime] = None  # When the next instance is due
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the recurrence pattern after initialization."""
        if not self.task_id:
            raise ValueError("Task ID must be provided for recurrence pattern")
        
        if self.interval <= 0:
            raise ValueError("Interval must be positive")
        
        if self.days_of_week:
            for day in self.days_of_week:
                if day < 0 or day > 6:
                    raise ValueError("Days of week must be between 0-6 (0=Monday, 6=Sunday)")
        
        if self.day_of_month is not None and (self.day_of_month < 1 or self.day_of_month > 31):
            raise ValueError("Day of month must be between 1-31")
        
        for exc_date in self.exceptions:
            if not isinstance(exc_date, date):
                raise ValueError("Exceptions must be date objects")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the recurrence pattern to a dictionary representation."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "pattern_type": self.pattern_type.value,
            "interval": self.interval,
            "days_of_week": self.days_of_week,
            "day_of_month": self.day_of_month,
            "exceptions": [exc.isoformat() for exc in self.exceptions],
            "end_condition": self.end_condition.to_dict() if self.end_condition else None,
            "next_occurrence": self.next_occurrence.isoformat() if self.next_occurrence else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class RecurrencePatternWithTask(RecurrencePattern):
    """
    Extends RecurrencePattern to include the associated task.
    """
    task: Optional[Any] = None  # Using Any to avoid circular import