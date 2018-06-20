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
from state import State
log = logger()

def main(controller):
    events = logic.globalDict['BlockStateEvents']
    own = controller.owner
    block = BlockProperties(own)
    
    if block.isMatchingStaticBlock():
        handleEvent(block, controller, events['onMatch'])
    else:
        handleEvent(block, controller, events['onMisMatch'])
    
def handleEvent(block, controller, event):
    onMatchChange = controller.sensors['onMatchChange']
    
    if onMatchChange.positive:
        cleanUpPrevStates(block)
    else:
        states =  getStatesToExec(block, event)
        execStates(block, states, event['default'])

def getStatesToExec(block, event):
    states = []

    if 'default' in event:
        states = event['default']

    if 'ifWasAmatchBefore' in event:
        if block.wasMatchingStaticBlock():
            states = event['ifWasAmatchBefore']

    if 'ifWasNotAmatchBefore' in event:
        if not block.wasMatchingStaticBlock():
            states = event['ifWasNotAmatchBefore']
    
    return states

def applyState(block, state, defaults=None):
    '''
    {
        stateObj : object,
        args: {},
        duration : { 'time' : 0, 'expiryActions':[]},
        delay : 0,
        scope: []
    }
    '''

    state = State(block, state)
    
    if state.hasScope and not state.hasCurBlockInScope:
        if defaults is not None:
            execStates(block, defaults)
        return 0

    if not state.isDelaySet and not state.isDurationSet:
        state.runAction()
    else:
        if state.isDelaySet and state.isDurationSet:
            delayAndRunStateInDuration(state)

        elif state.isDelaySet:
            delayState(state)
            
        elif state.isDurationSet:
            runStateInDuration(state)
        
def delayAndRunStateInDuration(state):
    state.startDelay()
    
    if state.isDelayExp:
        runStateInDuration(state)

def delayState(state):
    state.startDelay()
    
    if state.isDelayExp:
        state.runAction()

def runStateInDuration(state):
    state.startDuration()
    
    if not state.isDurationExp:
        state.runAction()
    else:
        actions = state.expiryActions
        execStates(state.block, actions)

def execStates(block, states, defaults=None):
    for state in states:
        applyState(block, state, defaults)

def cleanUpPrevStates(block):
    blockID = 'b%s' % block.getBlockNumber()

    if blockID not in logic.globalDict:
        return False
    
    bStates = logic.globalDict[blockID]['states']

    for stateName, props in bStates.items():
        state = State(block, props)
        resetTimer(state)

def resetTimer(state):
    if state.isDelaySet and state.isDelayTimerActive:
        state.cancelDelay()
    
    if state.isDurationSet and state.isDurationTimerActive:
        state.cancelDuration()

    