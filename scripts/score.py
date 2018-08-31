from bge import logic
from block import SpaceBlock, LogicalBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from utils import *
from copy import deepcopy
from navigator import overlayAssessment, SceneHelper
from widgets import Text
from canvas import NotificationCanvas
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
    if not chainList:
        return
    highestChain = logic.globalDict['MatchChainCount']
    chainLen = len(chainList)
    curindex = chainLen -1
    curChainBlock = chainList[curindex]
    curChainBlockLen = len(curChainBlock)
 
    if curChainBlockLen <= 0:
        return

    curChainBlock.sort()
    if (curChainBlockLen == 1 or
        chainList.count(curChainBlock) > 1):
         curChainBlock.clear()
    else:
        chainList.append([])

        if curChainBlockLen > highestChain:
            shelper = SceneHelper(logic)
            scene = shelper.getscene('HUD')
            node = scene.objects['notification_position_node']
            notification = NotificationCanvas(logic, 'HUD')
            notification.add('chain_notification', node)
            Text(notification.infoTxtObj, '%s Matches in a row!!' % curChainBlockLen)
            notification.startDuration(3.0)
            logic.globalDict['MatchChainCount'] = curChainBlockLen

def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']
    
    if game.status != 'STOPPED' and matchCount >= totalBlocks:
        game.stop()
        overlayAssessment()