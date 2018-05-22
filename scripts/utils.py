#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains generic utility methods that
#              can be reused throughout the program.
#########################################################
from bge import logic

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

