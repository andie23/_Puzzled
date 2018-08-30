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
        buildChain(block.blockID)
        if block.blockID not in matchList:
            matchList.append(block.blockID)
    else:
        resetChain()
        if block.blockID in matchList:
            matchList.remove(block.blockID)

def buildChain(blockID):
    chainList = logic.globalDict['MatchChainList']

    if len(chainList) == 0:
        chainList.append([])

    curindex = len(chainList) -1
    if blockID not in chainList[curindex]:
        chainList[curindex].append(blockID)

def resetChain():
    chainList = logic.globalDict['MatchChainList']
    chainLen = len(chainList)
    curindex = chainLen -1
    curChainBlock = chainList[curindex]

    if len(curChainBlock) <= 0:
        return

    curChainBlock.sort()
    if (len(curChainBlock) == 1 or
        chainList.count(curChainBlock) > 1):
         curChainBlock.clear()      
    else:
         chainList.append([])            

def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']
    print(logic.globalDict['MatchChainList'])
    if game.status != 'STOPPED' and matchCount >= totalBlocks:
        game.stop()
        overlayAssessment()