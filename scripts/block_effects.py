from bge import logic
from logger import logger
from utils import animate
from playback import PlayBack

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
TRANSPARENT = [0.0, 0.0, 0.0, 0.3]
RED = [1.0, 0.007, 0.0, 1.0]

def use_red_color(block):
    block.color = RED

def use_match_color(block):
    block.color = MATCH_COLOR

def use_default_color(block):
    block.color = DEFAULT_COLOR

def use_transparent(block):
    block.color = TRANSPARENT

def animate_red_flashes(block, speed=1.0, duration=0.0, delay=0.0,
     onstartAction=None, onfinishAction=None):

    return _animateLoop(
        obj = block, 
        animation='red_flash',
        fstart=0.0,
        fstop=5.0,
        duration=duration,
        delay=delay,
        speed=speed,
        onstartAction=onstartAction, 
        onfinishAction=onfinishAction
    )    

def animate_default_color(block, speed=0.8, duration=0.0, delay=0.0,
     onstartAction=None, onfinishAction=None):

    return _animateOnce(
        obj = block, 
        animation='fade_in_def_col',
        fstart=0.0,
        fstop=5.0,
        duration=duration,
        delay=delay,
        speed=speed,
        onstartAction=onstartAction, 
        onfinishAction=onfinishAction
    )

def animate_match_color(block, speed=0.8, duration=0.0, delay=0.0,
     onstartAction=None, onfinishAction=None):
    
    return _animateOnce(
        obj = block, 
        animation='fade_in_match_color',
        fstart=0.0,
        fstop=5.0,
        duration=duration,
        delay=delay,
        speed=speed,
        onstartAction=onstartAction, 
        onfinishAction=onfinishAction
    )

def animate_to_transparent(block, speed=0.4, duration=0.0, delay=0.0,
     onstartAction=None, onfinishAction=None):

    return _animateOnce(
        obj = block, 
        animation='fade_out_block',
        fstart=0.0,
        fstop=20.0,
        duration=duration,
        delay=delay,
        speed=speed,
        onstartAction=onstartAction, 
        onfinishAction=onfinishAction
    )

def _animateOnce(obj, animation, fstart, fstop, speed=1.0,
     duration=0.0, delay=0.0, onstartAction=None, onfinishAction=None):
   
    playback = PlayBack(
        obj=obj, animation=animation, fstart=fstart, 
        fstop=fstop, speed=speed
    )

    playback.play(duration=duration, delay=delay, onstartAction=onstartAction,
        onfinishAction=onfinishAction)
    return playback

def _animateLoop(obj, animation, fstart, fstop, speed=1.0,
     duration=0.0, delay=0.0, onstartAction=None, onfinishAction=None):

    playback = PlayBack(
        obj=obj, animation=animation, fstart=fstart, 
        fstop=fstop, speed=speed
    )

    playback.playLoop(delay=delay, duration=duration, onstartAction=onstartAction,
         onfinishAction=onfinishAction)
    return playback
