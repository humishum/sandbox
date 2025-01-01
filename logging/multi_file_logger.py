import logging

# create a logger 
logger = logging.getLogger("multi_file_logger")
logger.setLevel(logging.DEBUG)  # set root log level 
# not necessarily needed, but if we have multiple handlers, we can set level for each handler,
#  without having to adjust here the level of the main logger

# A handler is the component that actaully outputs the log. to for example the stream or file. 
# make separate file handlers and then also a stream handler.  
file_handler_1 = logging.FileHandler('logfile_1.log')
file_handler_1.setLevel(logging.DEBUG)  # note

file_handler_2 = logging.FileHandler('logfile_2.log')
file_handler_2.setLevel(logging.WARNING)  # note

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) # note

# create formeat for logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_1.setFormatter(formatter)
file_handler_2.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add handles to the logger
logger.addHandler(file_handler_1)
logger.addHandler(file_handler_2)
logger.addHandler(console_handler)

logger.debug("This is a DEBUG message.")  
logger.info("This is an INFO message.")  
logger.warning("This is a WARNING message.")  
logger.error("This is an ERROR message.")  
logger.critical("This is a CRITICAL message.")  



# # Log messages with different severity
# logger.debug("This is a DEBUG message.")  # Will go to logfile_1.log only
# logger.info("This is an INFO message.")   # Will go to logfile_1.log only
# logger.warning("This is a WARNING message.")  # Will go to both logfile_1.log and logfile_2.log
# logger.error("This is an ERROR message.")  # Will go to both logfile_1.log and logfile_2.log
# logger.critical("This is a CRITICAL message.")  # Will go to both logfile_1.log and logfile_2.log
