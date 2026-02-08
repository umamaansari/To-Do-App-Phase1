"""
Unit tests for the NotificationService.
"""
import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from src.services.notification_service import NotificationService
from src.services.task_store import TaskStore
from src.models.reminder_settings import ReminderSettings, ReminderTiming


class TestNotificationService:
    """Test cases for the NotificationService."""
    
    def setup_method(self):
        """Set up the test fixture."""
        self.task_store = TaskStore()
        self.notification_service = NotificationService(self.task_store)
    
    def test_calculate_notification_time_before_due(self):
        """Test calculating notification time for 'before_due' timing."""
        # Create a reminder setting
        reminder_settings = ReminderSettings(
            timing=ReminderTiming.BEFORE_DUE,
            minutes_before=30
        )
        
        # Mock a task with a due date
        from src.models.task import Task
        task = Task(
            title="Test Task",
            due_date=datetime.now() + timedelta(hours=2)  # Due in 2 hours
        )
        self.task_store.add_task(task)
        reminder_settings.task_id = task.id
        
        # Calculate notification time
        notification_time = self.notification_service._calculate_notification_time(reminder_settings)
        
        assert notification_time is not None
        # The notification should be 30 minutes before the due date
        expected_time = task.due_date - timedelta(minutes=30)
        assert abs((notification_time - expected_time).total_seconds()) < 60  # Within 1 minute tolerance
    
    def test_calculate_notification_time_at_due_time(self):
        """Test calculating notification time for 'at_due_time' timing."""
        # Create a reminder setting
        reminder_settings = ReminderSettings(
            timing=ReminderTiming.AT_DUE_TIME
        )
        
        # Mock a task with a due date
        from src.models.task import Task
        task = Task(
            title="Test Task",
            due_date=datetime.now() + timedelta(hours=1)  # Due in 1 hour
        )
        self.task_store.add_task(task)
        reminder_settings.task_id = task.id
        
        # Calculate notification time
        notification_time = self.notification_service._calculate_notification_time(reminder_settings)
        
        assert notification_time is not None
        # The notification should be at the due date
        assert abs((notification_time - task.due_date).total_seconds()) < 60  # Within 1 minute tolerance