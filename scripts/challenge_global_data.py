from patterns import PUZZLE_PATTERNS_4X4
from block_behavior_map import BLOCK_BEHAVIORS
from global_dictionary import GlobDict

CHALLENGE_DATA = {
    'id' : '',
    'name' : '', 
    'pattern' : '',
    'behavior' : '',
    'instructions': ''
}

class LoadedChallengeGlobalData(GlobDict):
    def __init__(self, challenge = None):
        super(LoadedChallengeGlobalData, self).__init__()
        if 'loaded_challenge' not in self.globDict:
            self.globDict['loaded_challenge'] = CHALLENGE_DATA
        
        if challenge:
            self.globDict['loaded_challenge'] = challenge

        self.data = self.globDict['loaded_challenge']

    def getId(self):
        return self.data['id']
    
    def getName(self):
        return self.data['name']
    
    def getInstructions(self):
        return self.data['instructions']

    def getPattern(self):
        return PUZZLE_PATTERNS_4X4[self.data['pattern']]

    def getBehavior(self):
        return BLOCK_BEHAVIORS[self.data['behavior']]

    def setId(self, id):
        self.data['id'] = id
    
    def setName(self, name):
        self.data['name'] = name
    
    def setInstructions(self, instructions):
        self.data['instructions'] = instructions

    def setPattern(self, pattern):
        self.data['pattern'] = pattern
