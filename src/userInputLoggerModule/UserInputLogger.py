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
LOG_NAME = "UserInputLogger.log"
LOG_PATH = "{}\\{}".format(LOG_DIR, LOG_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
    setOptions(options="")
        not implemented
        
    start()
        starts a thread which loggs the user inputs
    
    stop()
        stops / joins the thread which loggs the user inputs  
    '''
    def __init__(self, shared_queue, push_queue_delay=10):
        setup_logger(LOGGER_NAME, LOG_PATH, logging.DEBUG)
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.info("initialised UserInputLogger")
        self.running = False
        self.shared_queue = shared_queue
        self.push_queue_delay = push_queue_delay
        
    def setOptions(self, options=""):
        self.logger.info("set options: {}".format(options))
        # TODO: implement

    def on_press(self, key):
        return str(key)
    
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