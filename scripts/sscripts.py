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
    }
}