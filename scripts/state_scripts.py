from state import *

DEFAULT = {
    'onMatch' : { 
        'default' : [{ 
            'state' : {'obj': setMatchCol, 'args': {}},
            'duration' : 0,
            'delay': 0
        }]
    },
    'onMisMatch': {
        'default' : [{ 
            'state' : {'obj': setDefaultCol, 'args': {}},
            'duration': 0,
            'delay': 0
        }]
    }
}

