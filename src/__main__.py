import logging
import os
import time
from threading import Thread
from queue import Queue
from src.userInputLoggerModule.UserInputLogger import UserInputLogger
from src.concentrationEvaluatorModule.ConcentrationEvaluator import ConcentrationEvaluator
from src.concentrationEvaluatorModule.db import KeyloggerDatabase

MONGO_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "KeyloggerDB"
COLLECTION_NAME = "keylogs"

shared_queue = Queue()
database = KeyloggerDatabase(MONGO_URL, DATABASE_NAME, COLLECTION_NAME)
user_input_logger = UserInputLogger(shared_queue)
concentration_evaluator = ConcentrationEvaluator(shared_queue, database)
user_input_logger.start()
concentration_evaluator.start()
time.sleep(21)
user_input_logger.setOptions(logging_enabled=False)
concentration_evaluator.setOptions(logging_enabled=False)
time.sleep(21)
user_input_logger.stop()
concentration_evaluator.stop()