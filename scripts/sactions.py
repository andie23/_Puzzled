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
from animate import initAnimation, isAnimSet

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
COLOR_LESS = [0.0, 0.0, 0.0, 0.3]
RED = [1.0, 0.007, 0.0, 1.0]

#######################################
# COLOR MODES:
#######################################

def setDefaultCol(block):
    block.setColor(DEFAULT_COLOR)


def flashCol(block):
    state = logic.globalDict['BlockStates'][str(block.blockID)]
    
    if 'anim_id' not in state:
        animId = 'b%s_default_col' % block.blockID 
        initAnimation({
            'scene_id' : 'MAIN',
            'target_obj' : block.getVisualBlock(),
            'anim_name' : 'fade_in_def_col',
            'fstart' : 0.0, 
            'fstop' : 20.0, 
            'speed': 1.0
        }, animId)
        state.update({'anim_id' : animId}) 

def setMatchCol(block):
    state = logic.globalDict['BlockStates'][str(block.blockID)]

    if 'anim_id' not in state:
        animId = 'b%s_match_col' % block.blockID 
        initAnimation({
            'scene_id' : 'MAIN',
            'target_obj' : block.getVisualBlock(),
            'anim_name' : 'fade_in_match_color',
            'fstart' : 0.0, 
            'fstop' : 20.0, 
            'speed': 1.0
        }, animId)
        state.update({'anim_id' : animId}) 
    

def setRedCol(block):
    block.setColor(RED)

def setNoCol(block):
    state = logic.globalDict['BlockStates'][str(block.blockID)]
    if 'anim_id' not in state:
        animId = 'b%s_sen_no_col' % block.blockID 
        initAnimation({
            'scene_id' : 'MAIN',
            'target_obj' : block.getVisualBlock(),
            'anim_name' : 'fade_out_block',
            'fstart' : 0.0, 
            'fstop' : 20.0, 
            'speed': 1.0
        }, animId)
        state.update({'anim_id' : animId}) 
    
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
