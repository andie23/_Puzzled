import logging
from os import environ, mkdir

LOG_FILE_PATH = environ['HOMEPATH']
LOG_DIR_NAME  = 'puzzled'
LOG_FILE_NAME = 'puzzled.log'

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

'''
Return path of log file. Creates log directory if none exists
'''
def logPath():
    path = '{0}\{1}'.format(LOG_FILE_PATH, LOG_DIR_NAME)
    fullPath = '{0}\{1}'.format(path, LOG_FILE_NAME)
    
    if LOG_DIR_NAME not in LOG_FILE_PATH:
        mkdir(path)
            
    return fullPath
    
    