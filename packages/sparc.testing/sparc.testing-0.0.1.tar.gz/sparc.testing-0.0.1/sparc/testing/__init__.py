import sys
from sparc.logging import logging

logger = logging.getLogger() # root
def enableLogger(level = logging.DEBUG):
    logger.setLevel(level)

def disableLogger():
    logger.setLevel(logging.WARN)