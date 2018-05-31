from state import *

DEFAULT = {
    'onMatch' : { 
        'cleanUp': {},
        'states' : [{ 
            'state' : {'obj': setMatchCol, 'args': {}},
            'duration' : 0,
            'delay': 0
        }]
    },
    'onMisMatch': {
        'cleanUp' : {},
        'defaultActions' : [{ 
                'state' : {'obj': setDefaultCol, 'args': {}},
                'duration': 0,
                'delay': 0
            }]
        }
}


