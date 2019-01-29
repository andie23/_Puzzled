from bge import logic
from objproperties import ObjProperties
from utils import *
from copy import deepcopy
from navigator import overlayAssessment, SceneHelper
from notification import showNotification
from block import LogicalBlock
from game import *
import canvas

def updateMatchList(controller):
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, controller.owner)
    matchList = getPuzzleState('match_list')

    if block.isMatch:
        buildstreak(block.blockID)
        if block.blockID not in matchList:
            addMatch(block.blockID)
    else:
        resetstreak()
        if block.blockID in matchList:
            removeMatch(block.blockID)

def checkSequence():
    if not isSessionSet():
        return

    if (getGameStatus() != 'STOPPED' and 
        len(getPuzzleState('match_list')) >= getPuzzleState('block_count')):

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
        showNotification('Awesome!! achieved %s match streaks..' % streakLen)
        setPlayStats('match_streak', streakLen)
    streakList.clear()