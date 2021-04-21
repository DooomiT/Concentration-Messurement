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
        
    first_average_time : double
        time which will be taken to create the first average

    Methods
    ----------
    setOptions(logging_enabled=True, log_dir=None, logfile_name=None, push_queue_delay=None)
        changes the logging options
        
    start()
        starts a thread which loggs the user inputs
    
    stop()
        stops / joins the thread which loggs the user inputs  
    '''
    
    def __init__(self, shared_queue, first_average_time=10):
        self.logging_enabled = True
        self.initLoggerVariables()
        self.setupLogger()
        self.running = False
        self.shared_queue = shared_queue
        self.first_average_time = first_average_time
        self.first_average = None
        self.deleting_keys = ["delete", "backspace"]
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

    def getAmountAddingDeletingKeys(self, keys):
        amount_of_keys = len(keys)
        amount_of_deleting_keys = 0
        for key in self.deleting_keys:
            amount_of_deleting_keys += keys.count(key)
        amount_of_adding_keys = amount_of_keys - amount_of_deleting_keys
        return amount_of_adding_keys, amount_of_deleting_keys
    
    def evaluateAverageKeys(self, keys):
        amount_of_adding_keys, amount_of_deleting_keys = self.getAmountAddingDeletingKeys(keys)
        return amount_of_adding_keys / self.first_average_time

    def evaluateVarianceKeys(self, keys):
        #TODO: implement
        return 0

    def evaluateFirstConcentration(self, shared_queue):
        self.log(logging.debug, "evaluating first average for {} seconds".format(self.first_average_time))
        end_time = time.perf_counter() + self.first_average_time
        collected_keys = []
        while time.perf_counter() < end_time:
            user_input = shared_queue.get()
            collected_keys.extend(user_input)
            self.log(logging.debug, "received data: {}".format(user_input))
        self.first_average = self.evaluateAverageKeys(collected_keys)
        self.first_variance = self.evaluateVarianceKeys(collected_keys)
        self.log(logging.debug, "evaluated first - average = {}, variance = {}".format(self.first_average, self.first_variance))

    def evaluateNewConcentration(self, shared_queue):
        user_input = shared_queue.get()
        self.log(logging.debug, "received data: {}".format(user_input))
        current_average = self.evaluateAverageKeys(user_input)
        current_variance = self.evaluateVarianceKeys(user_input)
        self.log(logging.debug, "evaluated std - average = {}, variance = {}".format(self.current_concentration, self.current_variance))
        self.current_concentration = (self.first_average - current_average) + (self.first_variance - current_variance)
        self.log(logging.debug, "user concentration = {}".format(self.current_concentration))

    def run(self, shared_queue):
        while(self.running):
            if(self.first_average == None): self.evaluateFirstConcentration(shared_queue)
            self.evaluateNewConcentration(shared_queue)

    def start(self):
        self.log(logging.info, "started ConcentrationEvaluator")
        self.running = True
        self.thread = Thread(target = self.run, args = (self.shared_queue, ))
        self.thread.start()    

    def stop(self):
        self.log(logging.info,"stopped ConcentrationEvaluator")
        self.running = False
        self.thread.join()