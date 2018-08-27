from bge import logic
from block import SpaceBlock, LogicalBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from utils import *
from copy import deepcopy
from navigator import overlayAssessment
import game

log = logger()

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

    if game.status != 'STOPPED' and matchCount >= totalBlocks:
        game.stop()
        overlayAssessment()