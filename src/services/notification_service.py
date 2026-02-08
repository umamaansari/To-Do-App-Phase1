"""
NotificationService for managing notifications.
"""
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Optional
from src.models.reminder_settings import ReminderSettings
from src.services.task_store import TaskStore


class NotificationService:
    """
    Service for managing notifications and reminders.
    """
    
    def __init__(self, task_store: TaskStore):
        self.task_store = task_store
        self.active_timers = {}
        self.notification_callback: Optional[Callable[[str], None]] = None
    
    def set_notification_callback(self, callback: Callable[[str], None]):
        """
        Set the callback function to be called when a notification is triggered.
        """
        self.notification_callback = callback
    
    def schedule_notification(self, reminder_settings: ReminderSettings, task_title: str):
        """
        Schedule a notification based on reminder settings.
        """
        if not reminder_settings.enabled:
            return
        
        # Calculate when the notification should be sent
        notification_time = self._calculate_notification_time(reminder_settings)
        
        if notification_time is None:
            return
        
        # Cancel any existing timer for this reminder
        if reminder_settings.id in self.active_timers:
            self.active_timers[reminder_settings.id].cancel()
        
        # Calculate delay in seconds
        delay = (notification_time - datetime.now()).total_seconds()
        
        if delay <= 0:
            # Notification time has already passed, trigger immediately
            self._trigger_notification(f"🚨 URGENT REMINDER: \"{task_title}\" ab due hai!", reminder_settings)
            return
        
        # Create a timer to trigger the notification
        timer = threading.Timer(delay, self._trigger_notification, 
                              args=[f"🔔 Reminder: \"{task_title}\" is coming up!", reminder_settings])
        timer.start()
        
        # Store the timer so we can cancel it later if needed
        self.active_timers[reminder_settings.id] = timer
    
    def _calculate_notification_time(self, reminder_settings: ReminderSettings) -> Optional[datetime]:
        """
        Calculate when the notification should be sent based on reminder settings.
        """
        # Get the associated task to find its due date
        task = None
        for t in self.task_store.get_all_tasks():
            if t.id == reminder_settings.task_id:
                task = t
                break
        
        if not task or not task.due_date:
            return None
        
        if reminder_settings.timing == "at_due_time":
            return task.due_date
        elif reminder_settings.timing == "before_due" or reminder_settings.timing == "custom":
            if reminder_settings.minutes_before:
                return task.due_date - timedelta(minutes=reminder_settings.minutes_before)
        
        return None
    
    def _trigger_notification(self, message: str, reminder_settings: ReminderSettings):
        """
        Trigger the notification.
        """
        # Update the reminder settings to record when the notification was sent
        reminder_settings.last_reminder_sent = datetime.now()
        self.task_store.add_reminder_settings(reminder_settings)
        
        # Call the notification callback if available
        if self.notification_callback:
            self.notification_callback(message)
        else:
            # Default behavior: print the notification
            print(f"\n[NOTIFICATION] {message}\n")
    
    def cancel_notification(self, reminder_id: str):
        """
        Cancel a scheduled notification.
        """
        if reminder_id in self.active_timers:
            self.active_timers[reminder_id].cancel()
            del self.active_timers[reminder_id]
    
    def get_upcoming_notifications(self):
        """
        Get a list of upcoming notifications.
        """
        # This is a simplified implementation
        # In a real app, you'd track scheduled notifications
        return list(self.active_timers.keys())