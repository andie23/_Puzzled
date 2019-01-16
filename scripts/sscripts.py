from sactions import *

SCRIPTS = {
    'CLASSIC' : {
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
    }
}