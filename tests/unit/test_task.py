"""
Unit tests for the Task model.
"""
import pytest
from datetime import datetime
from src.models.task import Task, TaskStatus, TaskPriority


class TestTask:
    """Test cases for the Task model."""
    
    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task()
        
        assert task.id is not None
        assert task.title == ""
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.LOW
        assert task.created_at is not None
        assert task.updated_at is not None
    
    def test_task_creation_with_values(self):
        """Test creating a task with specific values."""
        title = "Test Task"
        description = "This is a test task"
        priority = TaskPriority.HIGH
        category = "work"
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            category=category
        )
        
        assert task.title == title
        assert task.description == description
        assert task.priority == priority
        assert task.category == category
    
    def test_task_title_length_validation(self):
        """Test that task title length is validated."""
        long_title = "x" * 201  # Exceeds 200 character limit
        
        with pytest.raises(ValueError):
            Task(title=long_title)
    
    def test_task_estimated_duration_validation(self):
        """Test that estimated duration validation works."""
        # Valid duration
        task = Task(title="Test", estimated_duration=30)
        assert task.estimated_duration == 30
        
        # Invalid duration (negative)
        with pytest.raises(ValueError):
            Task(title="Test", estimated_duration=-10)
        
        # Invalid duration (zero)
        with pytest.raises(ValueError):
            Task(title="Test", estimated_duration=0)
    
    def test_task_completion(self):
        """Test completing a task."""
        task = Task(title="Test Task")
        
        # Initially pending
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None
        
        # Complete the task
        task.complete()
        
        # Check status and completion time
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert task.updated_at >= task.completed_at
    
    def test_task_skip(self):
        """Test skipping a task."""
        task = Task(title="Test Task")
        
        # Initially pending
        assert task.status == TaskStatus.PENDING
        
        # Skip the task
        task.skip()
        
        # Check status
        assert task.status == TaskStatus.SKIPPED
        assert task.updated_at is not None
    
    def test_task_reopen(self):
        """Test reopening a completed task."""
        task = Task(title="Test Task")
        
        # Complete the task
        task.complete()
        assert task.status == TaskStatus.COMPLETED
        
        # Reopen the task
        task.reopen()
        
        # Check status
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            title="Test Task",
            description="Test Description",
            priority=TaskPriority.HIGH,
            category="work"
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["id"] == task.id
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["priority"] == "high"
        assert task_dict["category"] == "work"
        assert task_dict["status"] == "pending"