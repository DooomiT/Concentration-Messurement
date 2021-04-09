from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os
import time
from threading import Thread

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
    def __init__(self):
        logging.info("initialised UserInputLogger")
        pass
    
    def setOptions(self, options):
        logging.info("set options: {}".format(options))
        # TODO: implement
        pass
    
    def on_press(self, key):
        return str(key)
    
    def run(self):
        while(True):
            end_time = time.perf_counter() + LOG_DELAY_S
            keys = []
            while time.perf_counter() < end_time:   
                with keyboard.Events() as events:
                    event = events.get(LOG_DELAY_S)
                    if isinstance(event, keyboard.Events.Press):
                        keys.append("{}".format(event.key))
            logging.info("{} keys were pressed".format(len(keys)))
            # TODO: Pass keys somehow to the evaluation
                     
    def start(self):
        logging.info("started UserInputLogger")
        thread = Thread(target = self.run)
        thread.start()
        return thread
    
   
    
    
# TEST - TBR               
uil = UserInputLogger()
thread = uil.start()
time.sleep(10)
thread.join()
            