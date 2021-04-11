import logging
import os
import time
from threading import Thread
from queue import Queue

from src.helper.logger import setup_logger

LOGGER_NAME = "ConcentrationEvaluator"
LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOG_NAME = "ConcentrationEvaluator.log"
LOG_PATH = "{}\\{}".format(LOG_DIR, LOG_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class ConcentrationEvaluator:
    '''
        Input: logged User Data (time, data)
        Some Math
        Output: concentrationValue
        tbd: make nice docstring
    '''
    def __init__(self, shared_queue):
        setup_logger(LOGGER_NAME, LOG_PATH, logging.DEBUG)
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.info("initialised ConcentrationEvaluator")
        self.running = False
        self.shared_queue = shared_queue
    
    def setOptions(self, options):
        self.logger.info("set options: {}".format(options))
        # TODO: implement
    
    def run(self, shared_queue):
         while(self.running):
            userInput = shared_queue.get()
            self.logger.debug("received data: {}".format(userInput))
            # TODO: implement evaluation

    
    def start(self):
        self.logger.info("started ConcentrationEvaluator")
        self.running = True
        self.thread = Thread(target = self.run, args = (self.shared_queue, ))
        self.thread.start()    
    
    def stop(self):
        self.logger.info("stopped ConcentrationEvaluator")
        self.running = False
        self.thread.join()