"""
Simple persistent storage simulation using JSON files.
"""
import json
import os
from typing import Dict, Any, List
from src.models.task import Task
from src.models.user_profile import UserProfile
from src.models.recurrence import RecurrencePattern
from src.models.reminder_settings import ReminderSettings


class PersistentStorage:
    """
    Simple persistent storage simulation using JSON files.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.tasks_file = os.path.join(data_dir, "tasks.json")
        self.users_file = os.path.join(data_dir, "users.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
    
    def save_tasks(self, tasks: List[Dict[str, Any]]):
        """Save tasks to the tasks file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the tasks file."""
        with open(self.tasks_file, 'r') as f:
            return json.load(f)
    
    def save_users(self, users: List[Dict[str, Any]]):
        """Save users to the users file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_users(self) -> List[Dict[str, Any]]:
        """Load users from the users file."""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def clear_all(self):
        """Clear all stored data."""
        self.save_tasks([])
        self.save_users([])