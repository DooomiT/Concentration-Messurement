import logging
import os
import time
from threading import Thread
from queue import Queue

LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOG_PATH = "{}\\{}".format(LOG_DIR, "ConcentrationEvaluator.log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(filename = (LOG_PATH), level=logging.DEBUG, format='%(asctime)s: %(message)s')

class ConcentrationEvaluator:
    '''
        Input: logged User Data (time, data)
        Some Math
        Output: concentrationValue
        tbd: make nice docstring
    '''
    def __init__(self, shared_queue):
        logging.info("initialised ConcentrationEvaluator")
        self.running = False
        self.shared_queue = shared_queue
    
    def setOptions(self, options):
        logging.info("set options: {}".format(options))
        # TODO: implement
    
    def run(self):
         while(self.running):
            userInput = self.shared_queue.get()
            logging.debug("received data: {}".format(userInput))
            # TODO: implement evaluation

    
    def start(self):
        logging.info("started ConcentrationEvaluator")
        self.running = True
        self.thread = Thread(target = self.run, args = (self.shared_queue))
        self.thread.start()    
    
    def stop(self):
        logging.info("stopped ConcentrationEvaluator")
        self.running = False
        self.thread.join()