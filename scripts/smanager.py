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
from block import LogicalBlock
from bge import logic
from logger import logger
from state import State
log = logger()

def main(controller):
    events = logic.globalDict['eventScript']
    own = controller.owner
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, own)
    
    if block.isMatch:
        handleEvent(block, controller, events['onMatch'])
    else:
        handleEvent(block, controller, events['onMisMatch'])

def handleEvent(block, controller, event):
    onMatchChange = controller.sensors['on_match_change']
    
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
        if block.wasMatch:
            states = event['ifWasAmatchBefore']

    if 'ifWasNotAmatchBefore' in event:
        if not block.wasMatch:
            states = event['ifWasNotAmatchBefore']
    
    return states

def applyState(block, state, defaults=None):
    '''
    {
        stateObj : object,
        args: {},
        duration : { 
            'time' : 0, 
            'expiryActions':[], 
            'resetExp' : bool,
            'resetInit' : bool,
            'resetTimer' : bool,
        },
        delay : { 
            'time' : 0,
            'resetExp' : bool,
            'resetInit' : bool,
            'resetTimer' : bool,
        },
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
            delayAndRunStateInDuration(state, defaults)

        elif state.isDelaySet:
            delayState(state, defaults)
            
        elif state.isDurationSet:
            runStateInDuration(state)
        
def delayAndRunStateInDuration(state, defaults):
    state.startDelay()
    
    if state.isDelayExp:
        runStateInDuration(state)
    else:
        execStates(state.block, defaults)

def delayState(state, defaults):
    state.startDelay()
    
    if state.isDelayExp:
        state.runAction()
    else:
        execStates(state.block, defaults)

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
    blockId = str(block.blockID)
    if 'BlockStates' not in logic.globalDict:
        return

    if blockId in logic.globalDict['BlockStates']:
        bStates = logic.globalDict['BlockStates'][blockId]['states']
        for stateName, props in bStates.items():
            state = State(block, props)
            resetTimers(state)
            resetProps(state)

def resetProps(state):
    if state.isDelaySet:
        if state.isDelayExpReset:
            state.setIsDelayExp(False)
        
        if state.isDelayInitReset:
            state.setIsDelayInit(False)

    if state.isDurationSet:
        if state.isDurationExpReset:
            state.setIsDurationExp(False)
        
        if state.isDurationInitReset:
            state.setIsDurationInit(False)

def resetTimers(state):
    if  (state.isDelaySet and state.isDelayTimerReset 
          and state.isDelayTimerActive):
        
        state.cancelDelay()
    
    if (state.isDurationSet and state.isDurationTimerReset 
        and state.isDurationTimerActive):
        
        state.cancelDuration()

    