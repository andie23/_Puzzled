####################################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains logic for applying various 
#              states to an object. A list of states to apply
#              is defined in globalDict states and these states are 
#              executed based on predefined conditions. I.E.
#              if a state is defined to change color upon match
#              then the matchColorState will be applied to the object
#              if it's in the correct position or is a match.
#####################################################################
from puzzle import BlockProperties
from bge import logic
from logger import logger
from states import *
from utils import getPercentageOf

log = logger()

def main(controller):
    '''
    Execute default states defined for all objects
    '''

    states = logic.globalDict['states']
    own = controller.owner
    block = BlockProperties(own)
    execStates(block, controller, states)

def applyDefaultState(block):
    '''
    Apply default color to the block
    '''

    setDefaultCol(block)

def applyNoColorState(block):
    '''
    Disable color of the block
    '''

    setNoCol(block)

def applyMatchState(block, controller, onMisMatchActions):
    '''
    Applies match color state if block matches staticblock.
    However, if the block does not match the staticblock, states
    defined in "onMisMatchActions" dictionary are executed.
    '''

    if block.isMatchingStaticBlock():
        setMatchCol(block)
        clearStates(block)
    elif block.wasMatchingStaticBlock(): 
        execStates(block, controller, onMisMatchActions)

def applyAlertModeState(block, duration, controller, expiryAction):
    '''
    This is a timer based state where the block flashes an alert color
    until the timer duration runsout. Once the timer runsout, states defined
    in expiryAction are executed.
    '''
    
    # If the method is running in standalone mode, always check if the block
    # is already matching a static block
    if block.isMatchingStaticBlock() and block.isInAlertMode():
        stopAlertMode(block)
        return True
    # apply default state if the timer while in alert mode expired
    elif block.isAlertModeExpired():
        execStates(block, controller, expiryAction)
    else:
        # initiate alert mode
        if (not block.isMatchingStaticBlock() and not block.isInAlertMode()):
            startAlertMode(block)
            
        elif block.isInAlertMode():
            # get current time duration
            timerDuration = getCurrentAlertTimerDuration(block)
            
            # increase animation speed if percentage left is x
            if getPercentageOf(timerDuration, duration) >= 70:
                block.setAlertModeAnimSpeed(7.9)
    
            # stop the alertmode if timer runsout
            if timerDuration >= duration:
                log.debug('Block %s has expired on %s with duration set at %s', 
                            block.getBlockNumber(), timerDuration, duration)
                stopAlertMode(block, True)
                execStates(block, controller, expiryAction)  

def clearStates(block):
    '''
    Clear "special" states applied to the object
    '''

    if block.isMatchingStaticBlock() and block.isInAlertMode():
        stopAlertMode(block)
    
def execStates(block, controller, states):
    '''
    Executes states defined in states dictinary. Through definition name, appropriate
    methods are used for the defined state.
    '''
    
    if 'MATCH_STATE' in states:
        misMatchActions= states['MATCH_STATE']['onMisMatchActions']
        applyMatchState(block, controller=controller, onMisMatchActions=misMatchActions)
    
    if 'DEFAULT_STATE' in states:
        applyDefaultState(block)

    if 'ALERT_STATE' in states:
        alertState = states['ALERT_STATE']
        applyAlertModeState(
            block, controller=controller, 
            duration=alertState['duration'],
            expiryAction=alertState['expiryActions']
        )
    
    if 'NO_COLOR_STATE' in states:
        applyNoColorState(block)