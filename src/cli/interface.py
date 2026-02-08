"""
CLI interface for the AI Task Manager.
"""
import cmd
import sys
from datetime import datetime
from typing import Optional
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.task_store import TaskStore
from src.models.task import Task, TaskStatus, TaskPriority


class CLIInterface(cmd.Cmd):
    """
    Command Line Interface for the AI Task Manager.
    """
    
    intro = 'Welcome to the AI-Powered Task Manager for Umama! Type help or ? to list commands.\n'
    prompt = '> '
    
    def __init__(self):
        super().__init__()
        self.task_store = TaskStore()
        self.nlp_processor = NaturalLanguageProcessor()
        self.task_creation_service = TaskCreationService(self.nlp_processor, self.task_store)
    
    def default(self, line: str):
        """
        Handle natural language input for task creation.
        """
        if line.strip():
            try:
                task = self.task_creation_service.create_task_from_natural_language(line)
                print(f'Task "{task.title}" added successfully.')
                
                # Show updated list of pending tasks
                self.do_list("pending")
                
                # Check for overdue tasks and notify
                self._check_overdue_tasks()
                
            except Exception as e:
                print(f'Error processing task: {str(e)}')
    
    def do_add(self, arg: str):
        """
        Add a task using natural language.
        Usage: add <task_description>
        Example: add roz subah gym
                 add har Monday meeting 10 AM
        """
        if arg:
            try:
                task = self.task_creation_service.create_task_from_natural_language(arg)
                print(f'Task "{task.title}" added successfully.')
                
                # Show updated list of pending tasks
                self.do_list("pending")
                
                # Check for overdue tasks and notify
                self._check_overdue_tasks()
                
            except Exception as e:
                print(f'Error adding task: {str(e)}')
        else:
            print("Please provide a task description.")
    
    def do_list(self, arg: str):
        """
        List tasks with optional filtering.
        Usage: list [all|pending|completed|<category>|overdue]
        """
        if arg == 'all':
            tasks = self.task_store.get_all_tasks()
        elif arg == 'pending':
            tasks = self.task_store.get_tasks_by_status(TaskStatus.PENDING)
        elif arg == 'completed':
            tasks = self.task_store.get_tasks_by_status(TaskStatus.COMPLETED)
        elif arg == 'overdue':
            tasks = self._get_overdue_tasks()
        elif arg:  # Assume it's a category
            tasks = self.task_store.get_tasks_by_category(arg)
        else:
            tasks = self.task_store.get_tasks_by_status(TaskStatus.PENDING)
        
        if tasks:
            print("\nYour tasks:")
            for i, task in enumerate(tasks, 1):
                status_icon = "[DONE]" if task.status == TaskStatus.COMPLETED else "[PEND]"
                
                # Handle priority - check if it's an enum or string
                if isinstance(task.priority, TaskPriority):
                    priority_value = task.priority.value
                    priority_display = task.priority.value.upper()
                else:
                    # It's a string value
                    priority_value = task.priority
                    priority_display = task.priority.upper()
                
                priority_icon = "[HIGH]" if priority_value == "high" else "[MED]" if priority_value == "medium" else "[LOW]"
                
                due_str = f"📅 {task.due_date.strftime('%d %b %Y %I:%M %p')}" if task.due_date else "📅 No due date"
                
                # Handle datetime comparison - ensure both are timezone-aware or naive
                is_overdue = False
                if task.due_date:
                    # Get current time in the same timezone as the due date
                    if task.due_date.tzinfo is not None:
                        # due_date is timezone-aware, make now() timezone-aware too
                        current_time = datetime.now(task.due_date.tzinfo)
                    else:
                        # due_date is timezone-naive, make now() timezone-naive too
                        current_time = datetime.now().replace(tzinfo=None)
                    
                    is_overdue = task.due_date < current_time and task.status != TaskStatus.COMPLETED
                
                if is_overdue:
                    due_str = f"[OVERDUE] {task.due_date.strftime('%d %b %Y %I:%M %p')}"
                
                # Handle recurrence pattern type - check if it's an enum or string
                recurrence_str = ""
                if task.recurrence_pattern:
                    pattern_type = task.recurrence_pattern.get('pattern_type')
                    if hasattr(pattern_type, 'value'):
                        # It's an enum
                        pattern_type_value = pattern_type.value
                    else:
                        # It's a string
                        pattern_type_value = pattern_type
                    recurrence_str = f"[RECUR] {pattern_type_value}"
                
                reminder_str = f"[REMIND] {task.reminder_settings['minutes_before']} min before" if task.reminder_settings else ""
                
                print(f"• {status_icon} **{task.title}** | {priority_icon} {priority_display} | {due_str} {recurrence_str} {reminder_str}")
        else:
            print("No tasks found.")
    
    def _get_overdue_tasks(self) -> list:
        """Get a list of overdue tasks."""
        all_tasks = self.task_store.get_all_tasks()
        overdue_tasks = []
        
        for task in all_tasks:
            if task.due_date:
                # Handle datetime comparison - ensure both are timezone-aware or naive
                if task.due_date.tzinfo is not None:
                    # due_date is timezone-aware, make now() timezone-aware too
                    current_time = datetime.now(task.due_date.tzinfo)
                else:
                    # due_date is timezone-naive, make now() timezone-naive too
                    current_time = datetime.now().replace(tzinfo=None)
                
                if task.due_date < current_time and task.status != TaskStatus.COMPLETED:
                    overdue_tasks.append(task)
        
        return overdue_tasks
    
    def _check_overdue_tasks(self):
        """Check for overdue tasks and provide notification."""
        overdue_tasks = self._get_overdue_tasks()
        
        if overdue_tasks:
            print(f"\n[WARNING] You have {len(overdue_tasks)} overdue task(s)!")
            for task in overdue_tasks:
                print(f"  - {task.title} was due on {task.due_date.strftime('%d %b %Y %I:%M %p')}")
            print("  Yeh task 2 din se pending hai bhai, ab kar lete hain?")
    
    def do_complete(self, arg: str):
        """
        Mark a task as completed.
        Usage: complete <task_number_or_title>
        """
        if not arg:
            print("Please specify a task to complete.")
            return
        
        # Try to find the task by number first
        try:
            task_num = int(arg)
            pending_tasks = self.task_store.get_tasks_by_status(TaskStatus.PENDING)
            if 1 <= task_num <= len(pending_tasks):
                task = pending_tasks[task_num - 1]
                task.complete()
                self.task_store.update_task(task)
                print(f'Task "{task.title}" marked as completed.')
                
                # If the task has a recurrence pattern, create the next instance
                if task.recurrence_pattern:
                    self._create_next_recurrence_instance(task)
                
                # Show updated list
                self.do_list("pending")
                
                # Check for overdue tasks and notify
                self._check_overdue_tasks()
                return
        except ValueError:
            # Not a number, try to find by title
            pass
        
        # Find by title
        all_tasks = self.task_store.get_all_tasks()
        matching_tasks = [task for task in all_tasks if arg.lower() in task.title.lower()]
        
        if not matching_tasks:
            print(f"No task found containing '{arg}'")
            return
        
        if len(matching_tasks) > 1:
            print(f"Multiple tasks found containing '{arg}'. Please be more specific:")
            for i, task in enumerate(matching_tasks, 1):
                print(f"{i}. {task.title}")
            return
        
        task = matching_tasks[0]
        task.complete()
        self.task_store.update_task(task)
        print(f'Task "{task.title}" marked as completed.')
        
        # If the task has a recurrence pattern, create the next instance
        if task.recurrence_pattern:
            self._create_next_recurrence_instance(task)
        
        # Show updated list
        self.do_list("pending")
        
        # Check for overdue tasks and notify
        self._check_overdue_tasks()
    
    def _create_next_recurrence_instance(self, completed_task: Task):
        """
        Create the next instance of a recurring task.
        """
        # This is a simplified implementation
        # In a real app, you'd use the recurrence pattern to calculate the next occurrence
        print(f"Next instance of '{completed_task.title}' would be created based on recurrence pattern.")
    
    def do_skip(self, arg: str):
        """
        Skip a recurring task instance.
        Usage: skip <task_number_or_title>
        """
        if not arg:
            print("Please specify a task to skip.")
            return
        
        # Find by number or title (similar to complete)
        try:
            task_num = int(arg)
            pending_tasks = self.task_store.get_tasks_by_status(TaskStatus.PENDING)
            if 1 <= task_num <= len(pending_tasks):
                task = pending_tasks[task_num - 1]
                task.skip()
                self.task_store.update_task(task)
                print(f'Skipped task "{task.title}".')
                
                # Show updated list
                self.do_list("pending")
                
                # Check for overdue tasks and notify
                self._check_overdue_tasks()
                return
        except ValueError:
            pass
        
        # Find by title
        all_tasks = self.task_store.get_all_tasks()
        matching_tasks = [task for task in all_tasks if arg.lower() in task.title.lower()]
        
        if not matching_tasks:
            print(f"No task found containing '{arg}'")
            return
        
        if len(matching_tasks) > 1:
            print(f"Multiple tasks found containing '{arg}'. Please be more specific:")
            for i, task in enumerate(matching_tasks, 1):
                print(f"{i}. {task.title}")
            return
        
        task = matching_tasks[0]
        task.skip()
        self.task_store.update_task(task)
        print(f'Skipped task "{task.title}".')
        
        # Show updated list
        self.do_list("pending")
        
        # Check for overdue tasks and notify
        self._check_overdue_tasks()
    
    def do_delete(self, arg: str):
        """
        Delete a task.
        Usage: delete <task_number_or_title>
        """
        if not arg:
            print("Please specify a task to delete.")
            return
        
        # Find by number or title
        try:
            task_num = int(arg)
            all_tasks = self.task_store.get_all_tasks()
            if 1 <= task_num <= len(all_tasks):
                task = all_tasks[task_num - 1]
                if self.task_store.delete_task(task.id):
                    print(f'Task "{task.title}" deleted.')
                    
                    # Show updated list
                    self.do_list("pending")
                    
                    # Check for overdue tasks and notify
                    self._check_overdue_tasks()
                else:
                    print("Failed to delete task.")
                return
        except ValueError:
            pass
        
        # Find by title
        all_tasks = self.task_store.get_all_tasks()
        matching_tasks = [task for task in all_tasks if arg.lower() in task.title.lower()]
        
        if not matching_tasks:
            print(f"No task found containing '{arg}'")
            return
        
        if len(matching_tasks) > 1:
            print(f"Multiple tasks found containing '{arg}'. Please be more specific:")
            for i, task in enumerate(matching_tasks, 1):
                print(f"{i}. {task.title}")
            return
        
        task = matching_tasks[0]
        if self.task_store.delete_task(task.id):
            print(f'Task "{task.title}" deleted.')
            
            # Show updated list
            self.do_list("pending")
            
            # Check for overdue tasks and notify
            self._check_overdue_tasks()
        else:
            print("Failed to delete task.")
    
    def do_help(self, arg: str):
        """
        Show help information.
        """
        if not arg:
            print("Available commands:")
            print("  add <task>          - Add a task using natural language")
            print("  list [filter]       - List tasks (all, pending, completed, overdue, or category)")
            print("  complete <task>     - Mark a task as completed")
            print("  skip <task>         - Skip a recurring task instance")
            print("  delete <task>       - Delete a task")
            print("  help                - Show this help message")
            print("  quit/exit           - Exit the application")
            print("\nNatural Language Examples:")
            print("  > roz subah gym")
            print("  > har Monday meeting 10 AM")
            print("  > kal dopahar 2 baje doctor appointment")
        else:
            super().do_help(arg)
    
    def do_quit(self, arg: str):
        """
        Quit the application.
        """
        print("Goodbye! Take care, Umama!")
        return True
    
    def do_exit(self, arg: str):
        """
        Exit the application.
        """
        return self.do_quit(arg)
    
    def do_EOF(self, arg: str):
        """
        Handle EOF (Ctrl+D) to exit.
        """
        print()
        return self.do_quit(arg)