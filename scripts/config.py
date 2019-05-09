#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Data directory and button configurations are
#              defined here.
#########################################################
from os import environ

HOME_PATH = '{0}\{1}'.format(environ['HOMEDRIVE'],environ['HOMEPATH'])

'''
Databases and log file will be kept in DATA_DIR
'''

DATA_DIR  = 'puzzled'
LOG_FILE_NAME = 'puzzled.log'
DB_NAME = 'pcache'
SOUND_DIR = 'sound'

'''
Control button configuration
'''
BUTTON_CONFIG = {
    'UPARROWKEY' : 'UP',
    'DOWNARROWKEY' : 'DOWN',
    'LEFTARROWKEY' : 'LEFT', 
    'RIGHTARROWKEY': 'RIGHT' 
}
