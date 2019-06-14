from patterns import PUZZLE_PATTERNS_4X4
from block_behavior_map import BLOCK_BEHAVIORS
from global_dictionary import GlobDict

class LoadedChallengeGlobalData(GlobDict):
    def __init__(self, challenge = None):
        super(LoadedChallengeGlobalData, self).__init__('loaded_challenge')
        if challenge:
            self.setDefaults(
                challenge['id'], 
                challenge['name'], 
                challenge['pattern'],
                challenge['behavior'],
                challenge['instructions']    
            )
        elif not self.data:
            self.setDefaults()

    def setDefaults(self, id='', name='', pattern='', 
                    behavior='', instructions=''):

        self.data['id'] = id
        self.data['name'] = name
        self.data['pattern'] = pattern
        self.data['behavior'] = behavior
        self.data['instructions'] = instructions

    def getId(self):
        return self.data['id']
    
    def getName(self):
        return self.data['name']
    
    def getInstructions(self):
        return self.data['instructions']

    def getPattern(self):
        pattern = self.data['pattern']
        if pattern:
            return PUZZLE_PATTERNS_4X4[pattern]

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
