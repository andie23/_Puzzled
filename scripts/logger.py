import logging
from utils import logPath

'''
Returns logger object
'''
def logger():   
    path = logPath()
    logging.basicConfig(
        filename=path, level=logging.DEBUG,
        format='%(asctime)s: %(levelname)s: %(message)s'
    )
    return logging


    
    