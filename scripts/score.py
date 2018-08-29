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
    matchChainList = logic.globalDict['MatchChainList']
    
    if block.isMatch:
        logic.globalDict['MatchChainList'].append(block.blockID)
        if block.blockID not in matchList:
            logic.globalDict['MatchChainList'].append(block.blockID)
    else:
        if block.blockID in matchList:
            matchList.remove(block.blockID)
        print(matchList)
        logic.globalDict['MatchChainCount'] = len(matchChainList)
        log.debug('%s Blocks matched at once %s', logic.globalDict['MatchChainCount'], matchChainList)
        logic.globalDict['MatchChainList'] = []


def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']

    if game.status != 'STOPPED' and matchCount >= totalBlocks:
        game.stop()
        overlayAssessment()