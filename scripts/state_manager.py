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
    states =  processStatesToExec(event)
    execStates(block, controller, states)

def processStatesToExec(event):
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

def applyState(block, controller, stateDef):
    '''
    {
        state : { 'obj': object, 'args': {} }
        duration : 0,
        dalay : 0,
        scope: [],
        afterDurationActions: {}
    }
    '''

    state = StateHandler(stateDef, block, controller)
    
    if not state.isDelaySet() and not state.isDurationSet():
        state.run()
    else:
        if state.isDelaySet() and state.isDurationSet():
            delayAndRunStateInDuration(state)

        elif state.isDelaySet():
            delayState(state)
            
        elif state.isDurationSet():
            expActs = []
            if 'expiryActions' in stateDef:
                expActs = stateDef['expiryActions']    
            runStateInDuration(state, expActs)
        
def delayAndRunStateInDuration(state):
    state.startDelay()
    
    if state.isDelayExpired():
        runStateInDuration(state)

def delayState(state):
    state.startDelay()
    
    if state.isDelayExpired():
        state.run()

def runStateInDuration(state, expiryActions=[]):
    state.startDuration()
    
    if not state.isDurationExpired():
        state.run()
    else:
        if expiryActions:
            execStates( 
                state.block, state.controller, 
                expiryActions
            )
            
def cleanUp(block, actions):    
    blockNum = block.getBlockNumber()

    for action, props in actions.items():
        if 'TimerThreads' in props:
            cleanUpTthreads(
                blockNum, action, props.get('TimerThreads')
            )
        
        if 'StateProps' in props:
            resetStateProps(
                blockNum, action, props.get('StateProps')
            )

def cleanUpTthreads(blockNum, stateName, tStates):
    state = StateProps(blockNum, stateName)
    
    if '*' in tStates:
        state.cancelTthreads()
    else:
        for tState in tStates:
            tState = StateProps(blockNum, tState)
            tState.cancelTthread(tState._stateHeader)

def resetStateProps(blockNum, stateName, stateProps):
    state = StateProps(blockNum, stateName)
    
    if '*' in stateProps:
        state.setStateDefaults()
    else:
        for stateProp in stateProps:
            defaults = state.getStateDefaults()
          
            if stateProp in defaults:
                state.setStateProp(
                    stateProp, defaults.get(stateProp)
                )
    
def execStates(block, controller, states):
    for state in states:
        applyState(block, controller, state)
