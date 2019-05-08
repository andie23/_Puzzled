from block_states import *
from modes import *
from block_listerners import *

def default(block, onMatchListerner, onMisMatchListerner):
    onMatchListerner.attach('match_default_behavior', lambda: animate_match_color(block))
    onMisMatchListerner.attach('mis_match_default_behavior', lambda: animate_default_color(block))