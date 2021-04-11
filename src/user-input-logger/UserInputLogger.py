from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os
import time
from threading import Thread
from queue import Queue

# CONST
LOG_DELAY_S = 10
LOG_DIR = "{}{}".format(os.getcwd(), "\\logs")
LOG_PATH = "{}\\{}".format(LOG_DIR, "UserInputLogger.log")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(filename = (LOG_PATH), level=logging.DEBUG, format='%(asctime)s: %(message)s')

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
        logging.info("initialised UserInputLogger")
        self.running = False
        self.shared_queue = shared_queue
        
    def setOptions(self, options):
        logging.info("set options: {}".format(options))
        # TODO: implement

    def on_press(self, key):
        return str(key)
    
    def run(self):
        while(self.running):
            end_time = time.perf_counter() + LOG_DELAY_S
            keys = []
            while time.perf_counter() < end_time:   
                with keyboard.Events() as events:
                    event = events.get(LOG_DELAY_S)
                    if isinstance(event, keyboard.Events.Press):
                        keys.append("{}".format(event.key))
            self.shared_queue.put(keys)
            logging.info("send keys to ConcentrationEvaluator: {}".format(keys))

    def start(self):
        logging.info("started UserInputLogger")
        self.running = True
        self.thread = Thread(target = self.run)
        self.thread.start()    
    def stop(self):
        logging.info("stoped UserInputLogger")
        self.running = False
        self.thread.join()