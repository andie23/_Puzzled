from block_states import *
from block_listerners import *

def default(block, onMatchListerner, onMisMatchListerner):
    from audio import Audio
    from audio_files import SINGLE_DING

    onMatchListerner.attach('match_default_behavior', lambda: animate_match_color(block))
    onMatchListerner.attach('play_ring_sound', Audio(SINGLE_DING).play)
    onMisMatchListerner.attach('mis_match_default_behavior', lambda: animate_default_color(block))