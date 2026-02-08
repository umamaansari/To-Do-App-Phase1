#!/usr/bin/env python3
"""
Test script for the AI Task Manager application.
"""
import sys
import os

# Add the project root to the Python path so modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cli.interface import CLIInterface

def test_application():
    print("Initializing CLI...")
    cli = CLIInterface()
    print("CLI initialized successfully!")
    
    # Test adding a simple task
    print("\nTesting task addition...")
    try:
        # Simulate adding a task
        task_desc = "roz subah gym"
        cli.default(task_desc)
        print("Task added successfully!")
    except Exception as e:
        print(f"Error adding task: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_application()