#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Keyboard or mouse events are handled here, 
#              with appropriate movements applied to
#              puzzle blocks.
#########################################################
from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties
from config import BUTTON_CONFIG

DIRECTION_MAP = {
    'y+' : 'DOWN', 'y-': 'UP', 
    'x+' : 'LEFT', 'x-': 'RIGHT'
}

def init():
    logic.globalDict['MovableBlocks'] = {}

def spaceMain(controller):
    sensors = controller.sensors
    logic.globalDict['MovableBlocks'] = {}

    for sensor in sensors:
        sensorName = str(sensor)
        if sensorName not in DIRECTION_MAP:
            continue

        if sensor.hitObject:   
            block = ObjProperties(sensor.hitObject)
            blockNum = block.getProp('block_number')
            logic.globalDict['MovableBlocks'].update({
                '%s' % blockNum : sensorName
            })

def logicalMain(controller):
    own = controller.owner
    scene = logic.getCurrentScene()
    block = PuzzleBlockLogic(controller)
    blockNum = str(block.getBlockNumber())
    movableDirection = getMovableDirection(blockNum)
    
    if not movableDirection:
        return
    
    click = keyEvent(movableDirection, controller)
    sceneSpaceObj = scene.objects['space_block']
    spaceBlock = SpaceBlock(sceneSpaceObj)
    
    if click and not spaceBlock.isLocked():
        spaceBlock.lock()
        block.setIsMoving(True)
        block.setProp('cached_static_block', block.getCurrentStaticBlock())
        block.setProp('cached_space_direction', movableDirection)
        sceneSpaceObj.position = own.position

    if block.isMoving():
        moveBlock(block, spaceBlock)

def initMatchCheck(controller):
    own = controller.owner
    scene = logic.getCurrentScene()
    block = PuzzleBlockLogic(controller)
    block.matchBlockNumToStaticNum()

def getMovableDirection(bnum):
    if bnum not in logic.globalDict['MovableBlocks']:
        return None
    axis = logic.globalDict['MovableBlocks'][bnum]
    return DIRECTION_MAP[axis]

def moveBlock(block, spaceBlock):
    staticBlock = block.getCurrentStaticBlock()
    cachedStaticBlock = block.getProp('cached_static_block') 
    motionLoc = block.getMotionLoc(block.getProp('cached_space_direction'))
    
    cachedStaticNum = ObjProperties(cachedStaticBlock).getProp('block_number')
    
    if staticBlock is not None and staticBlock != cachedStaticBlock:
        block.snapToObj(staticBlock)
        block.setIsMoving(False)
        block.matchBlockNumToStaticNum()
        logic.globalDict['NumberOfMoves'] += 1
        spaceBlock.setProp('static_block_num', cachedStaticNum)
        block.setProp('cached_static_block', '')
        block.setProp('cached_space_direction', '')
        spaceBlock.unLock()
    else:
        block.move(motionLoc)

def keyEvent(movableDirection, cont):
    '''
    This is an input handler method. Currently, Mouse and Keyboard 
    input is supported. The gamer can switch between two inputs anytime during the game.
    
    Return: True or False if the input device is clicked or not
    '''

    keyboard  = cont.sensors['Keyboard']
    mouseNear = cont.sensors['MouseNear']
    mouseClick = cont.sensors['MouseClick']
    activeBtn = BUTTON_CONFIG[movableDirection]
    
    keyboard.key = activeBtn
        
    if  keyboard.positive:
        return True
    
    return True if mouseNear.positive and mouseClick.positive else False
