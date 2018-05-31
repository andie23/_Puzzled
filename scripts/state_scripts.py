from state import *


def getScript(name):
    if name in SCRIPTS:
        return SCRIPTS[name]

SCRIPTS = {

    'DEFAULT' : {
            'onMatch' : { 
                'cleanUp': {},
                'states' : [{ 
                    'state' : {'obj': setMatchCol, 'args': {}},
                    'duration' : 3,
                    'delay': 0,
                    'expiryActions' : [{
                        'state' : {'obj': setDefaultCol, 'args': {}},
                        'duration' : 0,
                        'delay': 0,
                    }]
                }]
            },
            'onMisMatch': {
                'cleanUp' : {
                        'setMatchCol': {
                            'TimerThreads' : ['setMatchCol'], 
                            'StateProps' : ['isDurationInit', 'isDurationExpired']
                        }        
                },
                'conditionalActions': {
                    'matchedBefore' : [{ 
                        'state' : {'obj': setDefaultCol, 'args': {}},
                        'duration': 0,
                        'delay': 0
                    }]
                }
            }
        }
}

