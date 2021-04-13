import logging
import os
import time
from threading import Thread
from queue import Queue
from src.userInputLoggerModule.UserInputLogger import UserInputLogger
from src.concentrationEvaluatorModule.ConcentrationEvaluator import ConcentrationEvaluator

shared_queue = Queue()
user_input_logger = UserInputLogger(shared_queue)
concentration_evaluator = ConcentrationEvaluator(shared_queue)
user_input_logger.start()
concentration_evaluator.start()
time.sleep(21)
user_input_logger.setOptions(logging_enabled=False)
time.sleep(21)
user_input_logger.stop()
concentration_evaluator.stop()