from bge import logic, events
from objproperties import ObjProperties
from config import BUTTON_CONFIG
from logger import logger
from block_listerners import *
from game import *
from audio_files import SLIDING_BLOCK
from audio import Audio

log = logger()

DIRECTION_MAP = {
    'y+': 'DOWN', 
    'y-': 'UP', 
    'x+': 'LEFT', 
    'x-': 'RIGHT'
}

def init(controller):
    '''
    Attach listerners for clicks, match and mismatch events.

    Note: This module is applicable to LogicalBlocks only. 
    Use an Always sensor for this module with PosPulse mode off.
    '''

    behavior = getBlockBehavior()
    block = LogicalBlock(logic.getCurrentScene(), controller.owner)
    slidingSound = Audio(SLIDING_BLOCK)
    
    behavior(
        block, OnMatchBlockListerner(block), OnMisMatchBlockListerner(block) 
    )
    
    OnClickBlockListerner(block).attach(
        'lock_space_block', lambda b,c,m,s: s.lock()
    )
    
    OnClickBlockListerner(block).attach(
        'start_block_slide', lambda b,c,m,s: startSlide(b,c,m,s)
    )
  
    OnBlockMovementStartListerner(block).attach(
        'play_sliding_sound', slidingSound.play
    )

    OnBlockMovementStopListerner(block).attach(
        'evaluate_match', lambda block, spaceBlock: evaluateMatch(block)
    )

    OnBlockMovementStopListerner(block).attach(
        'unlock_space_block', lambda block, spaceBlock: spaceBlock.unLock()
    )

    evaluateMatch(block)

def startSlide(block, controller, movableDirection, spaceBlock):
    '''
    Initiates block movement in direction set in movableDirection
    '''

    OnBlockMovementStartListerner(block).onStart()
    BlockMotion(controller.owner).start(movableDirection)

def evaluateMatch(block):
    if block.evaluateMatch():
        OnMatchBlockListerner(block).onMatch()
    else:
        OnMisMatchBlockListerner(block).onMisMatch()

def detectLogicalBlocks(controller):
    '''
    Detect blocks that can be moved by the player.

    This event should be triggered by a Sensor that checks

    Note: This module is Applicable to the SpaceBlock game object.
    '''
    scene = logic.getCurrentScene()
    sensors = controller.sensors

    clearMovableBlocks()

    for sensor in sensors:
        axisname = str(sensor)
        if axisname not in DIRECTION_MAP:
            continue
        if sensor.positive:
            block = LogicalBlock(scene, sensor.hitObject)
            addMovableBlock({
                str(block.blockID): DIRECTION_MAP[axisname]
            })
            OnDetectBlockListerner(block).onDetect(axisname)

def control(controller):
    '''
    Detects input events from the mouse and keyboard
    '''

    scene = logic.getCurrentScene()
    space = SpaceBlock(scene)
    
    if space.isLocked:
        return
    
    own = controller.owner
    block = LogicalBlock(scene, own)
    movableDirection = getMovableDirection(block.blockID)

    if isInputDetected(movableDirection, controller):
        OnClickBlockListerner(block).onClick(controller, movableDirection, space)

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
    bnum = str(bnum) 
    if bnum in getPuzzleState('movable_blocks'):
        return getPuzzleState('movable_blocks')[bnum]


def slide(controller):
    '''
    Applies motion to block until it senses a new position node a.k.a static
    block
    '''
    nodeDetector = controller.sensors['node_detector']
    isMove = controller.sensors['is_move']
    
    if not isMove.positive:
        return 

    own = controller.owner
    scene = logic.getCurrentScene()
    bmotion = BlockMotion(own)
    block = LogicalBlock(scene, own)
    space = SpaceBlock(scene)
    
    bmotion.slide()

    if (nodeDetector.positive and str(nodeDetector.hitObject) != str(block.positionNode)):
        space.setPosition(block.positionNode)
        bmotion.snapToObj(nodeDetector.hitObject)
        OnBlockMovementStopListerner(block).onStop(space)
        return

    OnBlockSlidingListerner(block).onSliding(bmotion)

class Block(ObjProperties):
    def __init__(self, scene, obj):
        super(ObjProperties, self).__init__()
        self.scene = scene
        self.blockObj = obj
        ObjProperties.__init__(self, self.blockObj)

    def setNode(self, node):
        self.setProp('position_node', str(node))

    @property
    def positionNode(self):
        node = self.getProp('position_node')
        if not node:
            return None
        return self.scene.objects[node]
    
    @property
    def positionNodeID(self):
        node = self.positionNode
        return node['block_number'] if node else 0
    
    @property
    def blockID(self):
        return self.getProp('block_number')

class SpaceBlock(Block):
    def __init__(self, scene):
        super(Block, self).__init__()
        Block.__init__(self, scene, scene.objects['space_block'])

    def setPosition(self, node):
        self.blockObj.position[0] = node.position[0]
        self.blockObj.position[1] = node.position[1]
        self.setNode(node)
    
    def detectNew(self):
        self.blockObj.sendMessage(
            '_sb_detect_lgblocks', '', str(self.blockObj)
        )

    @property
    def isLocked(self):
        return self.getProp('is_locked')
    
    def unLock(self):
        self.setProp('is_locked', False)
    
    def lock(self):
        self.setProp('is_locked', True)

class LogicalBlock(Block):
    def __init__(self, scene, obj):
        super(Block, self).__init__()
        Block.__init__(self, scene, obj)

    @property
    def isMatch(self):
        return self.getProp('is_match')

    @property
    def wasMatch(self):
        return self.getProp('was_match')

    def getVisualBlock(self):
        vsBlock = self.getProp('_visual_block')
        return self.scene.objects[vsBlock]

    def setColor(self, color):
        vsBlock = self.getVisualBlock()
        vsBlock.color = color

    def setMatch(self, boolval):
        return self.setProp('is_match', boolval)

    def setWasMatch(self, boolval):
        return self.setProp('was_match', boolval)

    def evaluateMatch(self):
        if not self.positionNode:
            return False

        if self.positionNodeID == self.blockID:
            self.setMatch(True)
            return True

        if self.positionNodeID != self.blockID:
            if self.isMatch:
                self.setWasMatch(True)
            self.setMatch(False)
            return False

class BlockMotion(ObjProperties):
    def __init__(self, blockObj):
        super(ObjProperties, self).__init__()
        ObjProperties.__init__(self, blockObj)
        self.blockObj = blockObj

    def getMotionLoc(self, direction):
        xAxis = 0
        yAxis = 1
        motionLoc = [0.0, 0.0, 0.0]
        speed = self.getProp('speed')
  
        if direction == 'UP':
            motionLoc[yAxis] = speed
        
        elif direction == 'DOWN':
            motionLoc[yAxis] = -speed
            
        elif direction == 'RIGHT':
            motionLoc[xAxis] = speed
        
        elif direction == 'LEFT':
            motionLoc[xAxis] = -speed
        
        return motionLoc

    def setIsInMotion(self, boolval):
        self.setProp('is_moving', boolval)

    @property
    def speed(self):
        return self.getProp('speed')

    @property
    def isInMotion(self):
        return self.getProp('is_moving')
    
    def start(self, direction):
        self.setProp('movable_direction', direction)
        self.setIsInMotion(True)

    def slide(self, direction=''):
        if not direction:
            direction = self.getProp('movable_direction')
        motionLoc = self.getMotionLoc(direction)
        self.applyMotionLoc(motionLoc)

    def applyMotionLoc(self, motionLoc):
        self.blockObj.applyMovement(motionLoc)

    def snapToObj(self, obj):
        self.blockObj.position[0] = obj.position[0]
        self.blockObj.position[1] = obj.position[1]
        self.setIsInMotion(False)
        self.setProp('position_node', str(obj))
        self.setProp('movable_direction', '')

