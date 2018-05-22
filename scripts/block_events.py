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
from logger import logger

def main(controller):
    own = controller.owner
    scene = logic.getCurrentScene()
    block = PuzzleBlockLogic(controller)
    click = keyEvent(block, controller)
    sceneSpaceObj = scene.objects['space_block']
    spaceBlock = SpaceBlock(sceneSpaceObj)
    
    if click and not spaceBlock.isLocked():
        # deactivate spaceblock from being detected
        # by other puzzle pieces to avoid conflicts
        spaceBlock.lock()
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
        sceneSpaceObj.position = own.position

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
        spaceBlock.unLock()
        block.setIsMoving(False)
        block.matchBlockNumToStaticNum()
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
