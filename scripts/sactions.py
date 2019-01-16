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
from game import *
from notification import showNotification

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
TRANSPARENT = [0.0, 0.0, 0.0, 0.3]
RED = [1.0, 0.007, 0.0, 1.0]

def use_red_color(block):
    block.setColor(RED)

def use_match_color(block):
    block.setColor(MATCH_COLOR)

def use_default_color(block):
    block.setColor(DEFAULT_COLOR)

def use_transparent(block):
    block.setColor(TRANSPARENT)

def animate_default_color(block):
    __runAnimationInstance(block, {
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_in_def_col',
        'fstart' : 0.0, 
        'fstop' : 5.0, 
        'speed': 1.0
    })

def animate_match_color(block):
    __runAnimationInstance(block, {
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_in_match_color',
        'fstart' : 0.0, 
        'fstop' : 5.0, 
        'speed': 1.0
    })

def animate_to_transparent(block):
    __runAnimationInstance(block, {
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_out_block',
        'fstart' : 0.0, 
        'fstop' : 20.0, 
        'speed': 1.0
    })

def flash_red_color(block, speed=1.5):
    animation = 'visual_block_red_flash' 
    animate(block.getVisualBlock(), animation, speed)

def __runAnimationInstance(block, data):
    state = logic.globalDict['BlockStates'][str(block.blockID)]
    animId = '%s_%s' % (block.blockID, data['anim_name'])
    
    if ('anim_id' not in state or 'anim_id' in state 
        and animId != state['anim_id']):
        
        initAnimation(data)
        state['anim_id'] = animId 
