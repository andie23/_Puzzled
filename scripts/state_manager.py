'''
The state manager module shall monitor the puzzle block and
change it's state accordingly based on parameters provided.

These states are asthetic in nature, such as:
    1. changing the color of the block when it's matching the correct static block,
    2. Entering an alert mode when a matched puzzle block is mismatched
    3. Changing the color of the puzzle block to black if alert mode timer runsout
'''

from puzzle import BlockProperties
from bge import logic
from logger import logger
import state

SCENE = logic.getCurrentScene()
CONT = logic.getCurrentController()
OWN = CONT.owner
CURRENT_BLOCK = BlockProperties(CONT.owner)
BLOCKNUM =  CURRENT_LOGICBLOCK.getBlockNumber()


def main():
    states = logic.globalDict['states']

    if MATCH_STATE in states:
        useMatchState()
        execMisMatchState(states)



def useMatchState():
    '''
    When the block's number is matching the current static block number, 
    change the color of the visualblock to indicate that it's in the correct
    position.
    '''

    if CURRENT_BLOCK.isMatchingStaticBlock():
        triggerState(SET_MATCH_COL_CODE, BLOCKNUM, OWN)

def execMisMatchState(states):
    if DEFAULT_STATE in states:
        useDefaultState()

    if ALERT_STATE in states:
        alertStateParams = states[ALERT_STATE]
        enterAlertMode(
            scope=alertStateParams['scope'], 
            duration=alertStateParams['duration'], 
            expiryAction=alertStateParams['expiryAction']
        )
    
    if DISCOLOR_STATE in states:
        rmColStateParams = states[DISCOLOR_STATE]
        removeColor(
            scope=rmColStateParams['scope'],
            offset=rmColStateParams['offset']
        )

    if PUZZLE_LOCK_STATE in states:
        pzlLocStateParams = states[PUZZLE_LOCK_STATE]
        lockPuzzleOnMismatches(
            misMatchCount=pzlLocStateParams['misMatchCount'],
            duration=pzlLocStateParams['duration']
        )


def useDefaultState():
    triggerState(SET_DEFAULT_COL_CODE, BLOCKNUM)

def removeColor(scope, offset=0):
    '''
    Remove color from puzzle block based on scope
    '''

    triggerState(DISABLE_COL_CODE, scope)

def enterAlertMode(scope, duration, expiryAction):
    '''
    When a puzzle block enters alertmode, this state will influence the puzzle
    block closest to it or all  blocks which are not matched. This can be set in the scope
  
    @param: scope: scope of influence nearest blocks or all blocks
    '''
    
    # check if already matched and not in alert mode
    if CURRENT_BLOCK.wasMatchingStaticBlock() and not CURRENT_BLOCK.isInAlertMode():
        timer = 0
        # Put blocks closest to 
        if scope == NEAREST:
            nearestBlocks = CURRENT_BLOCK.getNearestBlocks()
            for block in nearestBlocks:
                logicalBlock = BlockProperties(block)
                if not logicalBlock.isMatchingStaticBlock():
                    triggerState(
                        ACTIVATE_ALERT_MODE_CODE, 
                        logicalBlock.getBlockNumber()
                    )

        elif scope == CURRENT:
            triggerState(ACTIVATE_ALERT_MODE_CODE, BLOCKNUM)

        if timer >= duration:
            execMisMatchState(expiryAction)

def lockPuzzleOnMismatches(misMatchLimit, duration):
    '''
    Lock the puzzle if the maximum number of mismatches have been exceeded
    for a duration period.
    '''
    currentMismatches;

    if currentMismatches >= misMatchLimit:
        

def enterTimerMode(timeLimit, expiryAction=None):
    '''
    The game as a whole enters time trial state  
    '''
    pass

def lockPuzzle(duration):
    '''
    Lock the whole puzzle for a duration of time.
    @param: duration: determines how long the puzzle should be looked.
    '''
    timer = 0
    spaceObj = SCENE.objects['space_block']
    spaceBlock = puzzle.SpaceBlock(spaceObj)

        if timer <= duration:
            if not spaceBlock.isLocked():
                spaceBlock.lock()
        else:
            spaceBlock.unLock()
            timer = 0

def triggerState(code, blockScope, recBlock=None):
    subject = state.buildMsgSubj(code, blockScope)
    if recBlock is None:
        OWN.sendMessage(subject)
    else:
        OWN.sendMessage(subject, '', recBlock)
