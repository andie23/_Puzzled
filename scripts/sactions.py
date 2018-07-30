#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains method definitions of 
#              various states that can be applied to both
#              logical block and visualblock.
#########################################################
from puzzle import BlockProperties
from bge import logic
from logger import logger
from utils import animate

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
COLOR_LESS = [0.0, 0.0, 0.0, 0.3]

#######################################
# COLOR MODES:
#######################################
def setCol(block, col):
    scene = logic.getCurrentScene()
    visualBlock = BlockProperties(block.getVisualBlockObj(scene))
    visualBlock.setColor(col)

def setDefaultCol(block, args):
    setCol(block, DEFAULT_COLOR)

def setMatchCol(block, args):
    setCol(block, MATCH_COLOR)
        
def setNoCol(block, args):
    setCol(block, COLOR_LESS)

#########################################
# ALERT-MODE
#########################################

def setNormalRedFlash(block, args):
    _playRedFlash(block, args['speed'])

def setHyperRedFlash(block, args):
    _playRedFlash(block, args['speed'])

def _playRedFlash(block, speed):
    scene = logic.getCurrentScene()
    vsBlockObj = block.getVisualBlockObj(scene)
    visualBlock = BlockProperties(vsBlockObj)
       
    animation = 'visual_block_red_flash' 
    animate(vsBlockObj, animation, speed)
