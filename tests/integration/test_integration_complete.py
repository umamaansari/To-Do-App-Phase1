"""
Integration test to verify all components work together.
"""
import pytest
import os
from datetime import datetime, timedelta
from src.main import main
from src.cli.interface import CLIInterface
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.task_store import TaskStore
from src.models.task import Task, TaskStatus
from src.lib.persistent_storage import PersistentStorage


def test_complete_workflow_integration():
    """Test that all components work together in a complete workflow."""
    # Create a fresh task store for testing
    task_store = TaskStore(use_persistent_storage=False)  # Don't use persistent storage in tests
    nlp_processor = NaturalLanguageProcessor()
    task_creation_service = TaskCreationService(nlp_processor, task_store)
    
    # Test 1: Create a task using natural language
    task = task_creation_service.create_task_from_natural_language("urgent team meeting tomorrow at 10am")
    
    # Verify the task was created
    assert task is not None
    assert task.title != ""
    assert task.priority.name == "HIGH"  # Should be detected as high priority
    
    # Verify the task is in the store
    stored_task = task_store.get_task(task.id)
    assert stored_task is not None
    assert stored_task.title == task.title
    
    # Test 2: List tasks
    all_tasks = task_store.get_all_tasks()
    assert len(all_tasks) >= 1
    
    pending_tasks = task_store.get_tasks_by_status(TaskStatus.PENDING)
    assert len(pending_tasks) >= 1
    
    # Test 3: Update task status
    stored_task.complete()
    task_store.update_task(stored_task)
    
    # Verify the task is now completed
    completed_tasks = task_store.get_tasks_by_status(TaskStatus.COMPLETED)
    assert any(t.id == stored_task.id for t in completed_tasks)
    
    # Test 4: Delete task
    task_id = stored_task.id
    result = task_store.delete_task(task_id)
    assert result is True
    
    # Verify the task is gone
    deleted_task = task_store.get_task(task_id)
    assert deleted_task is None
    
    print("✓ All integration tests passed!")


def test_cli_integration():
    """Test CLI integration with all services."""
    cli = CLIInterface()
    
    # Temporarily redirect stdout to capture output
    import sys
    from io import StringIO
    original_stdout = sys.stdout
    captured_output = StringIO()
    
    try:
        sys.stdout = captured_output
        
        # Test adding a task via CLI
        cli.default("roz subah gym")
        output = captured_output.getvalue()
        assert "gym" in output.lower() or "task" in output.lower()
        
        # Reset the buffer
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Test listing tasks
        cli.do_list("pending")
        output = captured_output.getvalue()
        assert "gym" in output.lower() or "tasks" in output.lower()
        
        # Reset the buffer
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Test completing a task
        cli.do_complete("gym")
        output = captured_output.getvalue()
        assert "completed" in output.lower() or "marked" in output.lower()
        
    finally:
        sys.stdout = original_stdout
    
    print("✓ CLI integration tests passed!")


if __name__ == "__main__":
    test_complete_workflow_integration()
    test_cli_integration()
    print("✓ All integration tests completed successfully!")