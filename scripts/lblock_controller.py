from bge import logic, events
from config import BUTTON_CONFIG
from logger import logger
from block_listerners import *
from block import Block
from session_global_data import SessionGlobalData
from block_motion import BlockMotion
from lblock import LogicalBlock
from sblock import SpaceBlock

log = logger()
def init(controller):
    block = LogicalBlock(controller.owner)
    OnBlockInitListerner().onInit(block)

def initSlide(block, movableDirection):
    '''
    Initiates block movement in direction set in movableDirection
    '''
    log.debug('Block %s now sliding', block.blockID)
    BlockMotion(block.obj).start(movableDirection)
    OnBlockMovementStartListerner().onStart(block)

def onClick(controller):
    '''
    Detects input events from the mouse and keyboard
    '''

    space = SpaceBlock()
    
    if space.isLocked or space.isDisabled:
        return

    block = LogicalBlock(controller.owner)
    movableDirection = getMovableDirection(block.blockID)

    if isInputDetected(movableDirection, controller):
        log.debug('Player clicked on block %s', block.blockID)
        space.lock()
        initSlide(block, movableDirection)  
     
def isInputDetected(movableDirection, controller):
    if not movableDirection:
        return False
    
    if isMouseInput(controller):
        return True
    
    elif isKeyboardInput(movableDirection, controller):
        return True

def isMouseInput(controller):
    click = controller.sensors['click']
    hover = controller.sensors['hover']
    return click.positive and hover.positive

def isKeyboardInput(movableDirection, controller):
    keyboard = controller.sensors['keyboard']
    activeKeys = logic.keyboard.active_events

    if keyboard.positive:
        keyCode = keyboard.events[0][0]
        keyName = events.EventToString(keyCode)
        if keyName in BUTTON_CONFIG:
            return movableDirection == BUTTON_CONFIG[keyName]
    return False

def getMovableDirection(bnum):
    '''
    Searches globaldict if the blocknumber is in the 
    list of movable blocks
    '''
    
    movableBlocks = SessionGlobalData().getMovableBlocks()
    bnum = str(bnum)
    if bnum in movableBlocks:
        return movableBlocks[bnum]

def slide(controller):
    '''
    Applies motion to block until it senses a new position node a.k.a static
    block
    '''
    nodeDetector = controller.sensors['node_detector']
    own = controller.owner
    scene = logic.getCurrentScene()
    bmotion = BlockMotion(own)
    block = LogicalBlock(own)
    bmotion.slide()

    if (nodeDetector.positive and str(nodeDetector.hitObject) != str(block.positionNode)):
        log.debug('Block %s Sliding stopped.', block.blockID)
        SpaceBlock().setPosition(block.positionNode)
        bmotion.snapToObj(nodeDetector.hitObject)
        bmotion.suspendMovement()
        OnBlockMovementStopListerner().onStop(block)
