from bge import events
from os import environ, mkdir, listdir

HOME_PATH = environ['HOMEPATH']
'''
Databases and log file will be kept in DATA_DIR
'''
DATA_DIR  = 'puzzled'
LOG_FILE_NAME = 'puzzled.log'

'''
Control button configuration
'''
BUTTON_CONFIG = {
    'UP': events.UPARROWKEY,
    'DOWN' : events.DOWNARROWKEY,
    'LEFT' : events.LEFTARROWKEY,
    'RIGHT': events.RIGHTARROWKEY
}


'''
Return full path of the game's directory. The game directory is 
created if not found.
'''
def dataDirPath():
    path = '{0}\{1}'.format(HOME_PATH, DATA_DIR)
    
    if DATA_DIR not in listdir(HOME_PATH):
        mkdir(path)
         
    return path

'''
Returns full path of where the log file is located
'''
def logPath():
    return '{0}\{1}'.format(dataDirPath(), LOG_FILE_NAME)