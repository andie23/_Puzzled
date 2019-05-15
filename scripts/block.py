from bge import logic, events
from objproperties import ObjProperties
from config import BUTTON_CONFIG
from logger import logger
from block_listerners import *
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
    
    from challenge_global_data import LoadedChallengeGlobalData

    behavior = LoadedChallengeGlobalData().getBehavior()
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
    BlockMotion(controller.owner).start(movableDirection)
    OnBlockMovementStartListerner(block).onStart()
    OnBlockMovementListerner().onMove()

def evaluateMatch(block):
    if block.evaluateMatch():
        # Block specific listerners
        OnMatchBlockListerner(block).onMatch()
        # Non specific block listerners
        OnMatchListerner().onMatch()
    else:
        # Block specific listerners
        OnMisMatchBlockListerner(block).onMisMatch()
        # Non specific block listerners
        OnMisMatchListerner().onMisMatch()

def detectLogicalBlocks(controller):
    '''
    Detect blocks that can be moved by the player.

    This event should be triggered by a Sensor that checks

    Note: This module is Applicable to the SpaceBlock game object.
    '''

    from session_global_data import SessionGlobalData
    
    session = SessionGlobalData()
    scene = logic.getCurrentScene()
    sensors = controller.sensors

    session.clearMovableBlocks()

    for sensor in sensors:
        axisname = str(sensor)
        if axisname not in DIRECTION_MAP:
            continue
        if sensor.positive:
            block = LogicalBlock(scene, sensor.hitObject)
            session.setMovableBlock(str(block.blockID), DIRECTION_MAP[axisname])
            OnDetectBlockListerner(block).onDetect(axisname)

def control(controller):
    '''
    Detects input events from the mouse and keyboard
    '''

    scene = logic.getCurrentScene()
    space = SpaceBlock(scene)
    
    if space.isLocked or space.isDisabled:
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
    from session_global_data import SessionGlobalData
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
    
    @property
    def isDisabled(self):
        return self.getProp('is_disabled')

    def enable(self):
        self.setProp('is_disabled', False)
    
    def disable(self):
        self.setProp('is_disabled', True)

    @property
    def isLocked(self):
        return self.getProp('is_locked')
    
    def unLock(self):
        self.setProp('is_locked', False)
        log.debug('Spaceblock is locked')
    
    def lock(self):
        self.setProp('is_locked', True)
        log.debug('Spaceblock is now unlocked')

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

