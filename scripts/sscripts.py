from sactions import *

SCRIPTS = {
    'CLASSIC' : {
        'on_match' : {
            'default_state' : {
                'action' : setMatchCol
            }
        },
        'on_mismatch' : {
            'default_state' : {'action' : setDefaultCol},
            'if_matched_before' : {
                'action' : flashCol
            }
        }
    },
    'RED_ALERT' : {
        'on_match' : { 
            'default_state' : { 
                'action' : setMatchCol,
                'duration' : {
                    'time' : 3,
                    'callback': flashCol
                }
            }
        },
        'on_mismatch': {
            'default_state' : { 'action' : setDefaultCol},
            'if_matched_before': {
                'action' : setNormalRedFlash,
                'delay' : {
                    'time' : 2.0,
                    'action' : setRedCol
                },
                'duration' : {
                    'time': 4.0,
                    'callback': setGameOver
                }
            }
        }
    }
}