from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties

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
        spaceBlock.lock()
        print('Puzzle Complete')

    

