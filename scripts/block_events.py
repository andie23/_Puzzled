from bge import logic, events
from puzzle import PuzzleBlockLogic
from objproperties import ObjProperties
from config import BUTTON_CONFIG

def main(controller):
    own = controller.owner
    block = PuzzleBlockLogic(controller)
    click = keyEvent(block, controller)
    spaceBlock = getSpaceBlockObject()
    
    if click and not block.isMoving():
        if isSpaceBlockActivated():
            # deactivate spaceblock from being detected
            # by other puzzle pieces to avoid conflicts
            deactivateSpaceBloc()
            block.setIsMoving(True)
            # Cache the current location of the block
            # for later references.
            block.setProp(
                'cached_static_block', 
                block.getCurrentStaticBlock()
            )
            block.setProp(
                'cached_space_direction', 
                block.getSpaceBlockDirection()
            )
            spaceBlock.position = own.position

    if block.isMoving():
        moveBlock(block, spaceBlock)

def moveBlock(block, spaceBlock):
    '''
    Moves puzzle block until a static block is detected underneath it.
    Once in contact with a static block, the puzzle block is snapped into
    the center of the static block.. 
    
    Note: The space block is activated in this method after the puzzle block is snapped
    into position
    '''
    staticBlock = block.getCurrentStaticBlock()
    cachedStaticBlock = block.getProp('cached_static_block') 
    motionLoc = block.getMotionLoc(block.getProp('cached_space_direction'))
    
    if staticBlock is not None and staticBlock != cachedStaticBlock:
        # upon hitting the static block, we must align our
        # object to the static block's center
        block.snapToObj(staticBlock)
        block.setProp('cached_static_block', '')
        block.setProp('cached_space_direction', '')
        activateSpaceBloc()
        block.setIsMoving(False)
    else:
        block.move(motionLoc)

def keyEvent(block, cont):
    '''
    This is an input handler method. Currently, Mouse and Keyboard 
    input is supported. The gamer can switch between two inputs anytime during the game.
    
    Return: True or False if the input device is clicked or not
    '''
    keyboard  = cont.sensors['Keyboard']
    mouseNear = cont.sensors['MouseNear']
    mouseClick = cont.sensors['MouseClick']
    active_btn = block.getActiveDirectionalKey(BUTTON_CONFIG) 
    
    if active_btn is not None:
        if mouseNear.positive and mouseClick.positive:
            return True
        # assign dynamic key value to keyboard 
        keyboard.key = active_btn
        return keyboard.positive
    else:
        return False

def getSpaceBlockObject():
    scene = logic.getCurrentScene()
    return scene.objects['space_block']

def isSpaceBlockActivated():
    spaceBlockObj = getSpaceBlockObject()
    block = ObjProperties(spaceBlockObj)
    return  block.getProp('is_activated')

def deactivateSpaceBloc():
    spaceBlockObj = getSpaceBlockObject()
    spaceBlock = ObjProperties(spaceBlockObj)
    spaceBlock.setProp('is_activated', False)

def activateSpaceBloc():
    spaceBlockObj = getSpaceBlockObject()
    spaceBlock = ObjProperties(spaceBlockObj)
    spaceBlock.setProp('is_activated', True)