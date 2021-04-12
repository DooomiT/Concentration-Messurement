import pytest
import time
from queue import Queue

from src.userInputLoggerModule.UserInputLogger import UserInputLogger

def testInitQueue():
    test_queue = Queue()
    unitUnderTest = UserInputLogger(test_queue)
    assert unitUnderTest.shared_queue is test_queue
    assert unitUnderTest.push_queue_delay == 10
    assert not unitUnderTest.running
    
def testInitQueueDelay():
    test_queue = Queue()
    unitUnderTest = UserInputLogger(test_queue, 20)
    assert unitUnderTest.shared_queue is test_queue
    assert unitUnderTest.push_queue_delay == 20
    assert not unitUnderTest.running
    
def testThread():
    test_queue = Queue()
    unitUnderTest = UserInputLogger(test_queue, 0.01)
    unitUnderTest.start()
    unitUnderTest.stop()
    assert test_queue.qsize() > 0