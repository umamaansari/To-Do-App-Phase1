"""
Task model representing a single task with all its attributes and metadata.
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """
    Represents a single task with all its attributes and metadata.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.LOW
    category: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    notes: str = ""
    recurrence_pattern: Optional[Dict[str, Any]] = None
    reminder_settings: Optional[Dict[str, Any]] = None
    estimated_duration: Optional[int] = None

    def __post_init__(self):
        """Validate the task after initialization."""
        if len(self.title) > 200:
            raise ValueError("Task title must not exceed 200 characters")
        
        if self.estimated_duration is not None and self.estimated_duration <= 0:
            raise ValueError("Estimated duration must be positive if provided")

    def complete(self):
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def skip(self):
        """Mark the task as skipped."""
        self.status = TaskStatus.SKIPPED
        self.updated_at = datetime.now()

    def reopen(self):
        """Reopen a completed or skipped task."""
        self.status = TaskStatus.PENDING
        self.completed_at = None
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value,
            "priority": self.priority.value,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "notes": self.notes,
            "recurrence_pattern": self.recurrence_pattern,
            "reminder_settings": self.reminder_settings,
            "estimated_duration": self.estimated_duration
        }