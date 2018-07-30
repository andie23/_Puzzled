from sactions import *
from utils import RandNumScope

SCRIPTS = {
    'CLASSIC' : {
        'onMatch' : { 
            'default' : [{ 'stateObj' : setMatchCol }]
        },
        'onMisMatch': {
            'default' : [{ 'stateObj' : setDefaultCol }]
        }
    },
    'ALERT_MODE' : {
        'onMatch' : { 
            'default' : [{ 'stateObj' : setMatchCol }]
        },
        'onMisMatch': {
            'default' : [{ 'stateObj' : setDefaultCol }],
            'ifWasAmatchBefore': [{
                'stateObj' : setNormalRedFlash,
                'args' : {'speed': 1.5},
                'duration': {
                    'time' : 4,
                    'expiryActions':[{'stateObj' : setNoCol}]
                }
            }]
        }
    }
}