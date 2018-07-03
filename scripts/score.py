from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties
from pcache import *
from clock import getCurTime
from logger import logger

log = logger()

def updateMatch():
    globDict = logic.globalDict
    cont = logic.getCurrentController()
    block = PuzzleBlockLogic(cont)
    blockNumber = block.getBlockNumber()
    matchingBlocks = globDict['matchingBlocks']

    if blockNumber not in matchingBlocks:
        if block.isMatchingStaticBlock():
            matchingBlocks[blockNumber] = None
    else:
        if not block.isMatchingStaticBlock():
            del matchingBlocks[blockNumber]

def sequenceCheck():
    globDict = logic.globalDict
    matchingBlocks = globDict['matchingBlocks']
    totalBlocks = globDict['totalBlocks']
    matchingBlockCount = len(matchingBlocks)
    
    scene = logic.getCurrentScene()
    spaceBlock = SpaceBlock(scene.objects['space_block'])
    
    if matchingBlockCount >= totalBlocks:
        gstatus = globalDict['GameStatus'] 
        
        if gstatus['isActive']:
            finishTime = getCurTime()
            gstatus['isActive'] = False
            gstatus['finishTime'] = getCurTime()
            updateCacheScore(finishTime)
            spaceBlock.lock()

def updateCacheScore(finishTime):
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']

    score = Scores()

    prevScore = score.get(playerID, challenge)

    if not prevScore:
        log.debug('New high Score %s', finishTime)
        score.add(playerID, challenge, finishTime)
        return
    
    if finishTime > prevScore['complete_time']:
        log.debug('New high Score %s', finishTime)
        score.update(playerID, challenge, finishTime)
