import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Create a rotating file handler with a max size of 5MB and 3 backups
    rotating_handler = RotatingFileHandler(
        'app.log',  # Log file name
        maxBytes=5 * 1024 * 1024,  # Maximum file size before rotating (5MB)
        backupCount=3  # Number of backup log files to keep
    )

    # Set the logging format for the rotating handler
    rotating_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,  # Change to ERROR or WARNING in production
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Logs to console
            rotating_handler  # Logs to file with rotation
        ]
    )
