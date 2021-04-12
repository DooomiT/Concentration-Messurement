import pytest
from queue import Queue

from src.concentrationEvaluatorModule.ConcentrationEvaluator import ConcentrationEvaluator

def testInit():
    test_queue = Queue()
    unitUnderTest = ConcentrationEvaluator(test_queue)
    assert unitUnderTest.shared_queue is test_queue
    assert not unitUnderTest.running