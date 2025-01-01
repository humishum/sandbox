import logging

# Set up the logger
logging.basicConfig(filename="shared_output1.log",  # Log file name
                    level=logging.INFO,   # Set the log level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Log format

# Loop to write to the log file every 0.5 seconds
while True:
    logging.info("Log Entry from logger2")
    logging.warning("Log Entry from logger2")
    logging.error("Log Entry from logger2")
    
