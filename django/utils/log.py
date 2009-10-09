import logging

class NullHandler(logging.Handler): 
    def emit(self, record): 
        pass

logger = logging.getLogger('django') 
logger.addHandler(NullHandler()) 
logger.propagate = False
