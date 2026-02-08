"""
Performance test to verify the <2 second response time requirement.
"""
import time
import pytest
from src.services.nlp_service import NaturalLanguageProcessor
from src.services.task_creation_service import TaskCreationService
from src.services.task_store import TaskStore


def test_response_time_performance():
    """Test that the system responds within 2 seconds for task creation."""
    task_store = TaskStore(use_persistent_storage=False)
    nlp_processor = NaturalLanguageProcessor()
    task_creation_service = TaskCreationService(nlp_processor, task_store)
    
    # Measure time for task creation
    start_time = time.time()
    
    # Create a task using natural language
    task = task_creation_service.create_task_from_natural_language(
        "roz subah gym karna hai, zaroori hai"
    )
    
    end_time = time.time()
    
    # Calculate response time
    response_time = end_time - start_time
    
    print(f"Task creation response time: {response_time:.4f} seconds")
    
    # Verify the response time is under 2 seconds
    assert response_time < 2.0, f"Response time {response_time:.4f}s exceeds 2 second requirement"
    
    # Verify the task was created successfully
    assert task is not None
    assert task.title != ""
    
    print("✓ Performance test passed: Response time is under 2 seconds")


if __name__ == "__main__":
    test_response_time_performance()
    print("✓ All performance tests completed successfully!")