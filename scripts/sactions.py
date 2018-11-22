#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains method definitions of 
#              various states that can be applied to both
#              logical block and visualblock.
#########################################################
from bge import logic
from logger import logger
from utils import animate

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
COLOR_LESS = [0.0, 0.0, 0.0, 0.3]
RED = [1.0, 0.007, 0.0, 1.0]
#######################################
# COLOR MODES:
#######################################
def setDefaultCol(block):
    block.setColor(DEFAULT_COLOR)


def setMatchCol(block):
    block.setColor(MATCH_COLOR)

def setRedCol(block):
    block.setColor(RED)

def setNoCol(block):
    block.setColor(COLOR_LESS)

#########################################
# ALERT-MODE
#########################################

def setNormalRedFlash(block, speed=1.5):
    _playRedFlash(block, speed)

def setHyperRedFlash(block, speed=2.0):
    _playRedFlash(block, speed)

def _playRedFlash(block, speed):
    animation = 'visual_block_red_flash' 
    animate(block.getVisualBlock(), animation, speed)
