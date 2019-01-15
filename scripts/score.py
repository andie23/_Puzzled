from bge import logic
from block import SpaceBlock, LogicalBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from utils import *
from copy import deepcopy
from navigator import overlayAssessment, SceneHelper
from widgets import Text
from timer import Timer
from notification import showNotification
import game
import canvas
 

log = logger()

def updateMatchList(controller):
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, controller.owner)
    matchList = logic.globalDict['MatchingBlocks']
    
    if block.isMatch:
        buildChain(block.blockID)
        if block.blockID not in matchList:
            matchList.append(block.blockID)
    else:
        resetChain()
        if block.blockID in matchList:
            matchList.remove(block.blockID)

def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']
    status = game.getStatus()

    if status != 'STOPPED' and matchCount >= totalBlocks:
        hud = canvas.HudCanvas('HUD')
        timer = Timer('show_assessment_screen', 'HUD')
        hud.load()
        hud.disableWidgets()
        game.stop()
        showNotification('15 Puzzle Complete..', duration=5.0, callback=overlayAssessment)

def buildChain(blockID):
    chainList = logic.globalDict['MatchChainList']
    if blockID not in chainList:
        chainList.append(blockID)

def resetChain():
    chainList = logic.globalDict['MatchChainList']
    highestChainLen = game.getSessionVar('chain_count')
    chainLen = len(chainList)
    
    if chainLen > 1 and chainLen > highestChainLen:
        showNotification('Awesome!! achieved %s match streaks..' % chainLen)
        game.writeToSessionVar('chain_count', chainLen) 
    chainList.clear()