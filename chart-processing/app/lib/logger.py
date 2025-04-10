import logging

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")
LOGGER.addHandler(logging.StreamHandler())

def logInfo(message):
    LOGGER.info(message)

def logWarning(message):
    LOGGER.warning(message)

def logError(message):
    LOGGER.error(message)
