from sactions import *
SCRIPTS = {
    'CLASSIC' : {
        'mode' : {
            'time_trial' : {
                'limit': 0.45,
                'on_finish' : lambda:setGameOver(None)
            }
        },
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