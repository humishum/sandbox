import logging
from rich.logging import RichHandler

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)  # Set the desired log level

# Create a file handler
file_handler = logging.FileHandler("my_log.log")

# Create a Rich handler
rich_handler = RichHandler()

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(rich_handler)

# Log some messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")