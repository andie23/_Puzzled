from bge import logic
from logger import logger
from utils import animate
from playback import PlayBack

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
    PlayBack(
        obj=block, animation='fade_in_def_col',
        fstart=0.0, fstop=5.0
    ).play()

def animate_match_color(block):
    PlayBack(
        obj=block, animation='fade_in_match_color',
        fstart=0.0, fstop=5.0, speed=0.8
    ).play()

def animate_to_transparent(block):
    PlayBack(
        obj=block, animation='fade_out_block',
        fstart=0.0, fstop=20.0
    ).play()