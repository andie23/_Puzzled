from block_effects import *
from block_listerners import *
from audio import Audio
from audio_files import *

def default():
    def onMisMatch(block, wasMatch):
        if wasMatch:
           animate_default_color(block.getVisualBlock())

    OnBlockMovementStartListerner().attach(
        'play_slide_sound', lambda block: Audio(SLIDING_BLOCK).play()
    )

    OnMatchListerner().attach(
        'match_default_behavior', 
        lambda block: animate_match_color(
            block.getVisualBlock()
        )
    )

    OnMatchListerner().attach(
        'play_ring_sound', lambda block: Audio(SINGLE_DING).play()
    )

    OnMisMatchListerner().attach(
        'mis_match_default_behavior', 
        lambda block, wasMatch: onMisMatch(block, wasMatch)
    )



    