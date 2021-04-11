from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os
import time
from threading import Thread
from queue import Queue

from src.helper.logger import setup_logger

# CONST
LOG_DELAY_S = 10
LOGGER_NAME = "UserInputLogger"
LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOG_NAME = "UserInputLogger.log"
LOG_PATH = "{}\\{}".format(LOG_DIR, LOG_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class UserInputLogger:
    '''
        A Logger which logs the User Input based on several options
        tbd:
            make nice docstring
            implementation
            log to file or object?
            ....
    '''
    def __init__(self, shared_queue):
        setup_logger(LOGGER_NAME, LOG_PATH, logging.DEBUG)
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.info("initialised UserInputLogger")
        self.running = False
        self.shared_queue = shared_queue
        
    def setOptions(self, options):
        self.logger.info("set options: {}".format(options))
        # TODO: implement

    def on_press(self, key):
        return str(key)
    
    def run(self, shared_queue):
        while(self.running):
            end_time = time.perf_counter() + LOG_DELAY_S
            keys = []
            while time.perf_counter() < end_time:   
                with keyboard.Events() as events:
                    event = events.get(LOG_DELAY_S)
                    if isinstance(event, keyboard.Events.Press):
                        keys.append("{}".format(event.key))
            shared_queue.put(keys)
            self.logger.info("send keys to ConcentrationEvaluator: {}".format(keys))

    def start(self):
        self.logger.info("started UserInputLogger")
        self.running = True
        self.thread = Thread(target = self.run, args=(self.shared_queue, ))
        self.thread.start()   

    def stop(self):
        self.logger.info("stoped UserInputLogger")
        self.running = False
        self.thread.join()