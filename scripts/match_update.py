from bge import logic
from block import LogicalBlock
from block_listerners import OnBlockMovementStartListerner, OnMatchBlockListerner, OnMisMatchBlockListerner
from game_event_listerners import OnPuzzleCompleteListerner
from session_global_data import SessionGlobalData
from game import *

def init(controller):
    '''
    Add score based methods to Match Listerners
    Note: Applicable to LogicalBlocks only. Use an Always
    sensor with PosPulse mode off.
    '''

    session = SessionGlobalData()
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, controller.owner)
    blockId = block.blockID

    OnBlockMovementStartListerner(block).attach(
        'increment_moves', lambda: incrementMoves(session)
    )

    OnMatchBlockListerner(block).attach(
        'add_to_matchlist', lambda: addBlockToMatchList(blockId, session)
    )

    OnMisMatchBlockListerner(block).attach(
        'remove_from_matchlist', lambda: removeBlockFromMatchList(blockId, session)
    )
    
    OnMatchBlockListerner(block).attach(
        'build_streak', lambda: buildstreak(blockId, session)
    )

    OnMisMatchBlockListerner(block).attach(
        'reset_match_streak', lambda: resetstreak(session)
    )

def incrementMoves(session):
    moves = session.getMoves() + 1
    session.setMoves(moves)

def addBlockToMatchList(blockId, session):
    if blockId not in session.getMatchList():
        session.setBlockInMatchList(blockId)

def removeBlockFromMatchList(blockId, session):
    if blockId in session.getMatchList():
        session.removeBlockFromMatchList(blockId)

def buildstreak(blockId, session):
    if blockId not in session.getMatchStreakList():
        session.setBlockInStreakList(blockId)

def resetstreak(session):
    from notification import showNotification
    streakList = session.getMatchStreakList()
    curStreakCount = len(streakList)
    bestStreakCount = session.getStreakCount()

    if curStreakCount > 1 and curStreakCount > bestStreakCount:
        showNotification('WOW!! %s Match streaks in a row.. Keep it up!!' % curStreakCount)
        session.setStreakCount(curStreakCount) 
    session.clearStreakList()
