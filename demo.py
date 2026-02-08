#!/usr/bin/env python3
"""
Demonstration script for the AI Task Manager application.
"""
import sys
import os

# Add the project root to the Python path so modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cli.interface import CLIInterface

def demo_application():
    print("="*60)
    print("AI-Powered Task Manager for Umama - DEMONSTRATION")
    print("="*60)
    print()
    print("Initializing the application...")
    
    # Initialize the CLI interface
    cli = CLIInterface()
    print("[OK] Application initialized successfully!")
    print()
    
    print("Sample commands you can use:")
    print("1. add roz subah gym")
    print("2. add har Monday meeting 10 AM") 
    print("3. list pending")
    print("4. complete 1")
    print("5. help")
    print()
    
    print("The application supports natural language input in both English and Urdu.")
    print("Examples:")
    print("- 'roz subah gym' (daily morning gym)")
    print("- 'kal dopahar 2 baje doctor appointment' (tomorrow afternoon 2 o'clock doctor appointment)")
    print("- 'har month bill pay' (pay bills every month)")
    print()
    
    print("Features:")
    print("[OK] Natural language task creation")
    print("[OK] Task prioritization (high, medium, low)")
    print("[OK] Task categorization (work, study, personal, health, finance)")
    print("[OK] Recurring tasks support")
    print("[OK] Due date management")
    print("[OK] Overdue task notifications")
    print("[OK] Urdu-English code-switching support")
    print()
    
    print("To start using the application, run:")
    print("cd", os.path.dirname(os.path.abspath(__file__)), "&& python src/main.py")
    print()
    print("Try commands like:")
    print("> roz subah gym")
    print("> har Monday meeting 10 AM")
    print("> list all")
    print("> help")
    print()
    print("Application is ready to use!")

if __name__ == "__main__":
    demo_application()