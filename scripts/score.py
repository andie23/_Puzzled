from bge import logic
from block import SpaceBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from hudapi import HUD_Clock
from utils import *

log = logger()

def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']
    
    if matchCount >= totalBlocks:
        gstatus = globDict['GameStatus']
        if gstatus['isActive']:
            scene = logic.getCurrentScene()
            spaceBlock = SpaceBlock(scene)
            clock = HUD_Clock()
            clock.stop()
            spaceBlock.lock()
            gstatus['isActive'] = False
            showAssessment({
                'current_time' : clock.snapshot,
                'current_moves' : globDict['NumberOfMoves']
            })

def showAssessment(sessionRecord):
    logic.globalDict['play_session'] = sessionRecord
    logic.addScene('ASSESSMENT', 1)
