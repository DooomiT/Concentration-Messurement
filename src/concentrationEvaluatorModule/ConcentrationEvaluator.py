import logging
import os
import time
from threading import Thread
from queue import Queue

from src.helper.logger import setup_logger

LOGGER_NAME = "ConcentrationEvaluator"
LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOGFILE_NAME = "ConcentrationEvaluator.log"

class ConcentrationEvaluator:
    '''
    Wraps threading.Thread
    gets a users Key data from a queue and 
    evaluates them as concentration level
    
    Attributes
    ----------
    shared_queue : Queue
        queue where the keys will get pushed on

    Methods
    ----------
    setOptions(logging_enabled=True, log_dir=None, logfile_name=None, push_queue_delay=None)
        changes the logging options
        
    start()
        starts a thread which loggs the user inputs
    
    stop()
        stops / joins the thread which loggs the user inputs  
    '''
    
    def __init__(self, shared_queue):
        self.logging_enabled = True
        self.initLoggerVariables()
        self.setupLogger()
        self.running = False
        self.shared_queue = shared_queue
        self.log(logging.info,"initialised ConcentrationEvaluator")

    def initLoggerVariables(self):
        self.logger_name = LOGGER_NAME
        self.log_dir = LOG_DIR
        self.logfile_name = LOGFILE_NAME

    def setupLogger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_path = "{}\\{}".format(self.log_dir, self.logfile_name)
        setup_logger(self.logger_name, self.log_path, logging.DEBUG)
        self.logger = logging.getLogger(LOGGER_NAME)

    def setOptions(self, logging_enabled=None, log_dir=None, logfile_name=None, push_queue_delay=None):
        if logging_enabled: self.logging_enabled = logging_enabled
        if log_dir: self.log_dir = log_dir
        if logfile_name: self.logfile_name = logfile_name
        if push_queue_delay: self.push_queue_delay = push_queue_delay
        self.setupLogger()
        self.log(logging.info, "set options: {},{},{},{}".format(logging_enabled, log_dir, logfile_name, push_queue_delay))

    def log(self, log_type, log_string):
        if self.logging_enabled == False: return
        if log_type is logging.info: self.logger.info(log_string)
        elif log_type is logging.debug: self.logger.debug(log_string)

    def run(self, shared_queue):
        while(self.running):
            userInput = shared_queue.get()
            self.log(logging.debug, "received data: {}".format(userInput))
            # TODO: implement evaluation

    def start(self):
        self.log(logging.info, "started ConcentrationEvaluator")
        self.running = True
        self.thread = Thread(target = self.run, args = (self.shared_queue, ))
        self.thread.start()    

    def stop(self):
        self.log(logging.info,"stopped ConcentrationEvaluator")
        self.running = False
        self.thread.join()