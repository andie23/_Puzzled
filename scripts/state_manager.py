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
from state_registry import StateHandler, StateProps
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
    states =  processStatesToExec(block, event)
    execStates(block, controller, states)

def processStatesToExec(block, event):
    states = []

    if 'default' in event:
        states = event['default']
    else:
        if block.wasMatchingStaticBlock():
            if 'ifWasAmatchBefore' in event:
                states = event['ifWasAmatchBefore']
        else:
            if 'ifWasNotAmatchBefore' in event:
                states = event['ifWasNotAmatchBefore']
    
    return states

def applyState(block, controller, stateProps):
    '''
    {
        stateObj : object,
        args: {},
        duration : { 'time' : 0, 'expiryActions':[]},
        delay : 0,
        scope: []
    }
    '''
    state = StateHandler(stateProps, block, controller)
    
    if 'scope' in stateProps:
        if not block.getBlockNumber() in stateProps['scope']:
            return True

    if not state.isDelaySet() and not state.isDurationSet():
        state.run()
    else:
        if state.isDelaySet() and state.isDurationSet():
            delayAndRunStateInDuration(state)

        elif state.isDelaySet():
            delayState(state)
            
        elif state.isDurationSet():
            runStateInDuration(state)
        
def delayAndRunStateInDuration(state):
    state.startDelay()
    
    if state.isDelayExpired():
        runStateInDuration(state)

def delayState(state):
    state.startDelay()
    
    if state.isDelayExpired():
        state.run()

def runStateInDuration(state):
    state.startDuration()
    
    if not state.isDurationExpired():
        state.run()
    else:
        actions = state.expiryActions
        execStates(state.block, state.controller, actions)

def execStates(block, controller, states):
    for state in states:
        applyState(block, controller, state)
