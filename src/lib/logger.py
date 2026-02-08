import logging
import os
from datetime import datetime


class Logger:
    """
    Simple logging functionality for debugging and monitoring.
    """
    
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a logger
        self.logger = logging.getLogger('TaskManagerLogger')
        self.logger.setLevel(log_level)
        
        # Create a file handler that logs even debug messages
        log_file = os.path.join(log_dir, f"taskmanager_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create a console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        if not self.logger.handlers:  # Prevent adding handlers multiple times
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)


# Global logger instance
logger = Logger()