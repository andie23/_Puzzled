from sactions import *
from utils import RandNumScope

DEFAULT = {
    'onMatch' : { 
        'default' : [{ 'stateObj' : setMatchCol }]
    },
    'onMisMatch': {
        'default' : [{ 'stateObj' : setDefaultCol }]
    }
}

ALERT = {
    'onMatch' : { 
        'default' : [{ 'stateObj' : setMatchCol }]
    },
    'onMisMatch': {
        'default' : [{ 'stateObj' : setDefaultCol }],
        'ifWasAmatchBefore' : [
            {
                'stateObj': setNormalRedFlash,
                'delay': {'time': 2},
                'args' : {'speed': 2.0},
                'duration': {
                    'time' : 5.0,
                    'expiryActions': [
                        { 
                            'stateObj': setHyperRedFlash,
                            'args' : {'speed': 6.6},
                            'duration': {
                                'time' : 3.0,
                                'expiryActions' : [
                                    {'stateObj': setNoCol}
                                ]
                            }
                        }
                    ]
                }
            }    
        ]
    }
}

MISSING = {
    'onMatch' : { 
        'default' : [{ 'stateObj' : setMatchCol }]
    },
    'onMisMatch': {
        'default': [{ 'stateObj' : setDefaultCol }],
        'ifWasNotAmatchBefore' : [
            { 'stateObj' : setNoCol, 'scope' : RandNumScope(6, 15).get()}
        ],
        'ifWasAmatchBefore': [
            {
                'stateObj': setNormalRedFlash,
                'delay': {'time': 2},
                'args' : {'speed': 2.0},
                'scope' : [1, 6, 7],
                'duration': {
                    'time' : 5.0,
                    'expiryActions': [
                        { 
                            'stateObj': setHyperRedFlash,
                            'args' : {'speed': 6.6},
                            'duration': {
                                'time' : 3.0,
                                'expiryActions' : [
                                    {'stateObj': setNoCol}
                                ]
                            }
                        }
                    ]
                }
            }
        ],
        
    }
}    


