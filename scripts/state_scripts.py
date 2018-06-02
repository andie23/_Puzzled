from state import *

DEFAULT = {
    'onMatch' : { 
        'default' : [{ 
            'stateObj' : setMatchCol,
            'args': {},
            'duration': {'time' : 0, 'expiryActions':[]},
            'delay': 0
        }]
    },
    'onMisMatch': {
        'default' : [{ 
            'stateObj' : setDefaultCol,
            'args': {},
            'duration': {'time' : 0, 'expiryActions':[]},
            'delay': 0
        }]
    }
}

