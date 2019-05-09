from bge import logic
from objproperties import ObjProperties
from utils import *
from copy import deepcopy
from navigator import overlayAssessment, SceneHelper
from notification import showNotification
from block import LogicalBlock
from block_listerners import OnBlockMovementStartListerner, OnMatchBlockListerner, OnMisMatchBlockListerner
from game import *
import canvas

def init(controller):
    '''
    Add score based methods to Match Listerners

    Note: Applicable to LogicalBlocks only. Use an Always
    sensor with PosPulse mode off.
    '''

    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, controller.owner)
    matchList = getPuzzleState('match_list')
    blockId = block.blockID

    OnBlockMovementStartListerner(block).attach(
        'increment_moves', incrementMoves
    )

    OnMatchBlockListerner(block).attach(
        'add_to_matchlist', lambda: addBlockToMatchList(blockId, matchList)
    )

    OnMisMatchBlockListerner(block).attach(
        'remove_from_matchlist', lambda: removeBlockFromMatchList(blockId, matchList)
    )
    
    OnMatchBlockListerner(block).attach(
        'build_streak', lambda: buildstreak(blockId)
    )

    OnMisMatchBlockListerner(block).attach(
        'reset_match_streak', lambda: resetstreak()
    )

def incrementMoves():
    moves = getPlayStats('moves') + 1 
    setPlayStats('moves', moves)

def addBlockToMatchList(blockId, matchList):
    if blockId not in matchList:
        addMatch(blockId)

def removeBlockFromMatchList(blockId, matchList):
    if blockId in matchList:
        removeMatch(blockId)

def checkMatchList():
    '''
    Check if the puzzle is complete and ends the game.

    Note: This module is not applicable to LogicalBlocks. 
    It must be run by an independent Game Object within the same scene
    with an Always Sensor in PosPulse mode.
    '''

    if getGameStatus() == 'STOPPED':
        return
    if (len(getPuzzleState('match_list')) >= getPuzzleState('block_count')):
        stop()
        showNotification('15 Puzzle Complete..',
            duration=5.0, callback=overlayAssessment)

def buildstreak(blockID):
    streakList = getBlocksInMatchStreak()
    if blockID not in streakList:
        addMatchStreak(blockID)

def resetstreak():
    streakList = getBlocksInMatchStreak()
    streakLen = len(streakList)
    
    if streakLen > 1 and streakLen > getPlayStats('match_streak'):
        showNotification('WOW!! %s Match streaks in a row.. Keep it up!!' % streakLen)
        setPlayStats('match_streak', streakLen)
    streakList.clear()