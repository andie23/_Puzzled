#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains generic utility methods that
#              can be reused throughout the program.
#########################################################
from bge import logic
from config import HOME_PATH, DATA_DIR, LOG_FILE_NAME
from os import mkdir, listdir

def animate(object, name,  speed, start=0, end=20):
    '''
    Play animations on specified scene objects.
    '''

    layer = 0 
    priority = 1
    blendin = 1.0
    mode = logic.KX_ACTION_MODE_LOOP
    layerWeight = 0.0
    ipoFlags = 1
    
    object.playAction(name, start, end, layer, 
         priority, blendin, mode, layerWeight, ipoFlags, speed)

def getPercentageOf(curVal, maxVal):
    '''
    Get percentage of curVal and maxVal
    returns int
    '''

    diff = maxVal - curVal
    div = curVal/maxVal
    perc = div * 100
    
    return int(perc)


def dataDirPath():
    '''
    Return full path of the game's directory. The game directory is 
    created if not found.
    '''

    path = '{0}\{1}'.format(HOME_PATH, DATA_DIR)
    
    if DATA_DIR not in listdir(HOME_PATH):
        mkdir(path)
         
    return path


def logPath():
    '''
    Returns full path of where the log file is located
    '''
    
    return '{0}\{1}'.format(dataDirPath(), LOG_FILE_NAME)

