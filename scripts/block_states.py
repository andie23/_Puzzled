from bge import logic
from logger import logger
from utils import animate
from animate import initAnimation, isAnimSet

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
TRANSPARENT = [0.0, 0.0, 0.0, 0.3]
RED = [1.0, 0.007, 0.0, 1.0]

def use_red_color(block):
    block.setColor(RED)

def use_match_color(block):
    block.setColor(MATCH_COLOR)
    __setBlockState(block, 'use_match_color')

def use_default_color(block):
    block.setColor(DEFAULT_COLOR)
    __setBlockState(block, 'use_default_color')

def use_transparent(block):
    block.setColor(TRANSPARENT)
    __setBlockState(block, 'use_transparent_color')

def animate_default_color(block):
    __runAnimationState(block, 'animate_default_color',{
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_in_def_col',
        'fstart' : 0.0, 
        'fstop' : 5.0, 
        'speed': 1.0
    })

def animate_match_color(block):
    __runAnimationState(block, 'animate_match_color',{
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_in_match_color',
        'fstart' : 0.0, 
        'fstop' : 5.0, 
        'speed': 1.0
    })

def animate_to_transparent(block):
    __runAnimationState(block, 'animate_to_transparent', {
        'scene_id' : 'MAIN',
        'target_obj' : block.getVisualBlock(),
        'anim_name' : 'fade_out_block',
        'fstart' : 0.0, 
        'fstop' : 20.0, 
        'speed': 1.0
    })

def __getBlockstate(block):
    from session_global_data import SessionGlobalData
    session = SessionGlobalData()

    if block.blockID in session.getBlockStates():
       return session.getBlockState(block.blockID)
    return {}

def __setBlockState(block, state):
    from session_global_data import SessionGlobalData
    session = SessionGlobalData()
    session.setBlockState(block.blockID, state)

def __runAnimationState(block, stateId, data):
    if stateId != __getBlockstate(block):
        initAnimation(data)
        __setBlockState(block, stateId)