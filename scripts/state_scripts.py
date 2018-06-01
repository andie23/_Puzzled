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

ALERT_MODE = {
    'onMatch' : { 
        'cleanUp': {
                'setNormalRedFlash' : {
                    'StateProps' : ['isDurationInit'],
                    'TimerThreads' : ['setNormalRedFlash'] 
                },
                'setHyperRedFlash' : {
                    'StateProps' : ['isDurationInit'],
                    'TimerThreads' : ['setHyperRedFlash'] 
                }
        },
        'states' : [{ 
            'state' : {'obj': setMatchCol, 'args': {}},
            'duration' : 0,
            'delay': 0
        }]
    },
    'onMisMatch': {
        'cleanUp' : {},
        'conditionalActions' : {
            'ifMatchedBefore': [{ 
                'state' : {'obj': setNormalRedFlash, 'args': {'speed': 1.5}},
                'duration': 6,
                'delay': 0,
                'expiryActions' : [{
                    'state' : {'obj': setHyperRedFlash, 'args': {'speed': 5.4}},
                    'duration': 5,
                    'delay': 0,
                    'expiryActions' : [{
                          'state' : {'obj': setNoCol, 'args': {}},
                          'duration': 0,
                          'delay': 0,
                    }]
                }]
            }]
        } 
    }
}


