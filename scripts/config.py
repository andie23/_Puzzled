#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Data directory and button configurations are
#              defined here.
#########################################################
from bge import events
from os import environ

HOME_PATH = '{0}\{1}'.format(environ['HOMEDRIVE'],environ['HOMEPATH'])

'''
Databases and log file will be kept in DATA_DIR
'''

DATA_DIR  = 'puzzled'
LOG_FILE_NAME = 'puzzled.log'
DB_NAME = 'cache'

'''
Control button configuration
'''

BUTTON_CONFIG = {
    'UP': events.UPARROWKEY,
    'DOWN' : events.DOWNARROWKEY,
    'LEFT' : events.LEFTARROWKEY,
    'RIGHT': events.RIGHTARROWKEY
}