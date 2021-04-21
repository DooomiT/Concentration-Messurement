import logging
import os
import time
from threading import Thread
from queue import Queue
from src.userInputLoggerModule.UserInputLogger import UserInputLogger
from src.concentrationEvaluatorModule.ConcentrationEvaluator import ConcentrationEvaluator

FILE_NAME = "keylogger.out"
FILE_DIR = "{}//{}".format(os.getcwd(), "data")
FILE_PATH = "{}//{}".format(FILE_DIR, FILE_NAME)

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

shared_queue = Queue()
user_input_logger = UserInputLogger(shared_queue)
concentration_evaluator = ConcentrationEvaluator(shared_queue, FILE_PATH)
user_input_logger.start()
concentration_evaluator.start()
time.sleep(21)
user_input_logger.setOptions(logging_enabled=False)
concentration_evaluator.setOptions(logging_enabled=False)
time.sleep(21)
user_input_logger.stop()
concentration_evaluator.stop()
