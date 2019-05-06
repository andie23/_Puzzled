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
import animate
import game

log = logger()

def main(controller):
    events = game.getPuzzleState('block_script')
    own = controller.owner
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, own)
    
    if block.isMatch:
        handleEvent(block, controller, events['on_match'])
    else:
        handleEvent(block, controller, events['on_mismatch'])

def handleEvent(block, controller, event):
    def execState():
        stateStatus = runState(block, getActiveState(block, event))
        if stateStatus == 0:
            runState(block, event['default_state'])

    onMatchChange = controller.sensors['on_match_change']
    eventChange = block.getProp('is_event_change')

    if onMatchChange.positive or eventChange:
        if eventChange:
            block.setProp('is_event_change', False)
            game.setPuzzleState('block_states', {})
        cleanUpPrevStates(block)
    else:
        execState()

def getActiveState(block, event):
    if 'default_state' in event:
        state = event['default_state']

    if 'if_matched_before' in event:
        if block.wasMatch:
            state = event['if_matched_before']

    if 'if_not_matched_before' in event:
        if not block.wasMatch:
            state = event['if_not_matched_before']
    return state

def runState(block, state):
    '''
    {
        action : func,
        args: {},
        duration : { 
            'time' : 0, 
            'callback': func, 
            'resetExp' : bool,
            'resetTimer' : bool,
        },
        delay : { 
            'time' : 0,
            'resetExp' : bool,
            'resetTimer' : bool
        },
        scope: []
    }
    '''
    state = State(block, state)
    
    if state.hasScope and not state.isBlockInScope:
        return 0

    if not state.isDurOrDelSet:
        state.runAction()
        return
    if state.isDurAndDelSet:
        inDelay = delayState(state, False)
        if not inDelay:
            runStateInDuration(state)

    elif state.isDelaySet:
        delayState(state)
        
    elif state.isDurationSet:
        runStateInDuration(state)

def delayState(state, execAction=True):
    if not state.isDelayActive and not state.isDelayExp:
        state.startDelay()
    
    if state.isDelayExp:
        if execAction : state.runAction()
        return False
    state.delayAction()
    return True

def runStateInDuration(state):
    if not state.isDurationActive and not state.isDurationExp:
        state.startDuration()
    
    if not state.isDurationExp:
        state.runAction()
        return
    state.callbackAction()

def cleanUpPrevStates(block):
    blockId = str(block.blockID)
    states = game.getPuzzleState('block_states')

    if blockId in states:
        bStateRoot = states[blockId]
        bStates = bStateRoot['states']
        stopAnimations(bStateRoot)
        
        for stateName, props in bStates.items():
            state = State(block, props)
            resetTimers(state)
            resetProps(state)

def stopAnimations(bStateRoot):
    if 'anim_id' in bStateRoot:
        animId = bStateRoot['anim_id']

        if animate.isAnimSet(animId, 'MAIN'):
            animate.killAnimInstance(animId)
        del bStateRoot['anim_id']

def resetProps(state):
    if state.isDelaySet and state.isDelayExpReset:
        state.setDelayExpiry(False)

    if state.isDurationSet and state.isDurationExpReset:
        state.setDurationExpiry(False)

def resetTimers(state):
    if  (state.isDelaySet and state.isDelayTimerReset 
          and state.isDelayActive):
        state.cancelDelay()
    
    if (state.isDurationSet and state.isDurationTimerReset 
        and state.isDurationActive):
        state.cancelDuration()

    