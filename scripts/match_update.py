from bge import logic
from block import LogicalBlock
from block_listerners import OnBlockMovementStartListerner, OnMatchBlockListerner, OnMisMatchBlockListerner
from game_event_listerners import OnPuzzleCompleteListerner
from global_dictionary import *
from game import *

def init(controller):
    '''
    Add score based methods to Match Listerners

    Note: Applicable to LogicalBlocks only. Use an Always
    sensor with PosPulse mode off.
    '''

    session = PuzzleSessionGlobalData()
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
    session.moves += 1

def addBlockToMatchList(blockId, session):
    if blockId not in matchList:
        session.matchList.append(blockId)

def removeBlockFromMatchList(blockId, session):
    if blockId in matchList:
        session.matchStreakList.remove(blockId)

def buildstreak(session, blockID):
    if blockID not in puzzleEnv.matchStreakList:
        session.matchStreakList.append(blockID)

def resetstreak(session):
    streakList = session.matchStreakList
    curStreakCount = len(streakList)
    bestStreakCount = session.bestStreakCount

    if curStreakCount > 1 and curStreakCount > bestStreakCount:
        showNotification('WOW!! %s Match streaks in a row.. Keep it up!!' % streakLen)
        session.streakCount = streakLen
    session.matchStreakList.clear()