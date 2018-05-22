#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains method definitions of 
#              various states that can be applied to both
#              logical block and visualblock.
#########################################################
from puzzle import BlockProperties
from bge import logic
from logger import logger
from utils import animate

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
COLOR_LESS = [0.0, 0.0, 0.0, 0.3]

log = logger()
scene = logic.getCurrentScene()

#######################################
# COLOR MODES:
#######################################

def setDefaultCol(block):
    visualBlock = BlockProperties(block.getVisualBlockObj(scene))
    visualBlock.setColor(DEFAULT_COLOR)
    
          
def setMatchCol(block):
    visualBlock = BlockProperties(block.getVisualBlockObj(scene))
    visualBlock.setColor(MATCH_COLOR)
        
def setNoCol(block):
    visualBlock = BlockProperties(block.getVisualBlockObj(scene))
    visualBlock.setColor(COLOR_LESS)

#########################################
# ALERT-MODE
#########################################

def startAlertMode(block):
    '''
    This is the main entry point to start a block alert mode 
    '''

    log.debug('Starting Block %s alertmode.. Status %s', 
                block.getBlockNumber(), block.isInAlertMode())
    block.setProp('alert_timer', 0.0000)
    block.setAlertMode(True)
    block.setAlertModeAnimSpeed(0.0)

def stopAlertMode(block, isExpired=False):
    '''
    Stops alert mode animation and changes the property "isInAlertMode" to false.
    '''
    
    log.debug('Stopping Block %s alertmode... Status: %s, Expiry: %s', 
            block.getBlockNumber(), block.isInAlertMode(), 
            block.isAlertModeExpired())

    vsBlock = block.getVisualBlockObj(scene)
    vsBlock.stopAction(0)
    block.setAlertMode(False)
    block.setIsAlertModeExpired(isExpired)

def getCurrentAlertTimerDuration(block):
    return block.getProp('alert_timer')

def playAlertModeAnim(controller):
    '''
    Plays the Alert-Mode animation as long as isInAlertMode is true.
    '''

    own = controller.owner
    block = BlockProperties(own)
    vsBlockObj = block.getVisualBlockObj(scene)
    visualBlock = BlockProperties(vsBlockObj)
    
    if block.isInAlertMode():   
        animation = 'visual_block_red_flash'
        speed = block.getAlertModeAnimSpeed() 
        
        if speed <= 0.0:
            speed = block.getDefAlertModeAnimSpeed()
        
        animate(vsBlockObj, animation, speed)
