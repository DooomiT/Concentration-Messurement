from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os
import time
from threading import Thread
from queue import Queue

from src.helper.logger import setup_logger

# CONST
LOGGER_NAME = "UserInputLogger"
LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOGFILE_NAME = "UserInputLogger.log"

class UserInputLogger:
    '''
    Wraps threading.Thread
    Logs the users keyboard input and pushes it to a queue
    
    Attributes
    ----------
    shared_queue : Queue
        queue where the keys will get pushed on

    push_queue_delay : int = 10
        time delay between pushing data to the queue

    Methods
    ----------
    setOptions(options)
        options : Dict 
        not implemented
        
    start()
        starts a thread which loggs the user inputs
    
    stop()
        stops / joins the thread which loggs the user inputs  
    '''
    # TODO: update docstring

    def __init__(self, shared_queue, push_queue_delay=10):
        self.logging_enabled = True
        self.initLoggerVariables()
        self.setupLogger()
        self.running = False
        self.shared_queue = shared_queue
        self.push_queue_delay = push_queue_delay
        self.log(logging.info,"initialised UserInputLogger")

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

    def setOptions(self, logging_enabled=True, log_dir=None, logfile_name=None, push_queue_delay=None):
        self.logging_enabled = logging_enabled
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
            end_time = time.perf_counter() + self.push_queue_delay
            keys = []
            while time.perf_counter() < end_time:   
                with keyboard.Events() as events:
                    event = events.get(self.push_queue_delay)
                    if isinstance(event, keyboard.Events.Press):
                        keys.append("{}".format(event.key))
            shared_queue.put(keys)
            self.log(logging.info, "send keys to ConcentrationEvaluator: {}".format(keys))

    def start(self):
        self.log(logging.info,"started UserInputLogger")
        self.running = True
        self.thread = Thread(target = self.run, args=(self.shared_queue, ))
        self.thread.start()   

    def stop(self):
        self.log(logging.info,"stoped UserInputLogger")
        self.running = False
        self.thread.join()