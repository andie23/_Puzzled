from sactions import *
from modes import *

SCRIPTS = {
    'CLASSIC' : {
        'mode' : {
            'time_trial' : {
                'limit' : 15,
                'on_finish' : end_game_and_set_blocks_to_transparent
            }
        },
        'on_match' : {
            'default_state' : {
                'action' : animate_match_color
            }
        },
        'on_mismatch' : {
            'default_state' : {
                'action' : use_default_color
            },
            'if_matched_before' : {
                'action' : animate_default_color
            }
        }
    },
    'RED_ALERT' : {
        'on_match' : { 
            'default_state' : { 
                'action' : animate_match_color,
                'duration' : {
                    'time' : 3.0,
                    'callback': animate_default_color
                }
            }
        },
        'on_mismatch': {
            'default_state' : { 
                'action' : animate_default_color
            },
            'if_matched_before': {
                'action' : flash_red_color,
                'delay' : {
                    'time' : 2.0,
                    'action' : use_red_color
                },
                'duration' : {
                    'time': 4.0,
                    'callback': animate_to_transparent
                }
            }
        }
    },
    'NO_COLOR_MODE' : {
        'on_match' : {
            'default_state' : {
                'action' : animate_to_transparent
            }
        },
        'on_mismatch': {
            'default_state' : {
                'action' : animate_to_transparent
            }
        }

    }
}