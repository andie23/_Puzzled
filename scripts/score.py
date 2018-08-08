from bge import logic
from block import SpaceBlock, LogicalBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from hud import Clock
from utils import *
from copy import deepcopy
log = logger()

def init():
    logic.chainQueue = []
    logic.chainedBlocks = []

def refreshMatchList():
    obj = scene.objects['puzzle_main']
    obj.sendMessage('_refresh_match_list')

def updateMatchList(controller):
    scene = logic.getCurrentScene()
    block = LogicalBlock(scene, controller.owner)
    matchList = logic.globalDict['MatchingBlocks']     
    if block.isMatch:
        if block.blockID not in matchList:
            matchList.append(block.blockID)
    else:
        if block.blockID in matchList:
            matchList.remove(block.blockID)

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
            clock = Clock(logic)
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
