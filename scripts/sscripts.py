from sactions import *

SCRIPTS = {
    'CLASSIC' : {
        'on_match' : { 
            'default_state' : { 
                'action' : setMatchCol,
                'duration' : {
                    'time' : 3.0,
                    'callback': setDefaultCol
                }
            }
        },
        'on_mismatch': {
            'default_state' : { 'action' : setDefaultCol},
            'if_matched_before': {
                'action' : setNormalRedFlash,
                'delay' : {
                    'time' : 3.0,
                    'action' : setRedCol
                },
                'duration' : {
                    'time': 6.0,
                    'callback': setNoCol
                }
            }
        }
    }
}