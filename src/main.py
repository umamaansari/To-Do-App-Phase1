#!/usr/bin/env python3
"""
Main entry point for the AI-Powered Task Manager for Umama.
"""

import sys
import os
# Add the project root to the Python path so modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.interface import CLIInterface


def main():
    """Main function to start the AI Task Manager."""
    print("Assalam-o-Alaikum Umama! Aaj ka mood kaisa hai? Koi naya task add karein ya purane plan dekhein?")

    cli = CLIInterface()
    cli.cmdloop()


if __name__ == "__main__":
    main()