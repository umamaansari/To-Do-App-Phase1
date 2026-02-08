"""
Module for managing todo tasks in memory.
"""

from typing import List, Dict, Optional


class TodoManager:
    """
    Manages todo tasks in memory.
    """
    
    def __init__(self):
        """
        Initializes the TodoManager with an empty list of tasks.
        """
        self.tasks: List[Dict] = []
    
    def add_task(self, title: str, description: str = "") -> int:
        """
        Adds a new task with the given title and optional description.
        
        Args:
            title: The title of the task (required)
            description: The description of the task (optional)
            
        Returns:
            The ID of the newly created task
        """
        # Validate that title is not empty
        if not title.strip():
            raise ValueError("Title is required.")
        
        # Generate a unique ID (find max existing ID + 1)
        new_id = 1
        if self.tasks:
            existing_ids = [task["id"] for task in self.tasks]
            new_id = max(existing_ids) + 1
        
        # Create the new task
        task = {
            "id": new_id,
            "title": title,
            "description": description,
            "completed": False
        }
        
        # Add the task to the list
        self.tasks.append(task)
        
        return new_id
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Returns all tasks.
        
        Returns:
            A list of all tasks
        """
        return self.tasks
    
    def find_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Finds a task by its ID.
        
        Args:
            task_id: The ID of the task to find
            
        Returns:
            The task if found, None otherwise
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Updates the title and/or description of an existing task.
        
        Args:
            task_id: The ID of the task to update
            title: The new title (optional)
            description: The new description (optional)
            
        Returns:
            True if the task was updated, False if the task was not found
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False
        
        if title is not None:
            task["title"] = title
        if description is not None:
            task["description"] = description
        
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """
        Deletes a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False if the task was not found
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False
        
        self.tasks.remove(task)
        return True
    
    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggles the completion status of a task.
        
        Args:
            task_id: The ID of the task to toggle
            
        Returns:
            True if the task status was toggled, False if the task was not found
        """
        task = self.find_task_by_id(task_id)
        if task is None:
            return False
        
        task["completed"] = not task["completed"]
        return True