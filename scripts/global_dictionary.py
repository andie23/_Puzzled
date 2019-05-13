from bge import logic
from patterns import PUZZLE_PATTERNS_4X4
from block_behavior_map import BLOCK_BEHAVIORS

class GlobDict():
    def __init__(self):
        self.__globDict = logic.globalDict

class PuzzleSessionGlobalData(GlobDict):
    def __init__(self):
        GlobDict.__init__(self)
        if 'play_session' not in self.__globDict:
            self.__globDict['play_session'] =  {
                'play_session' : {
                    'moves' : 0,
                    'time' : 0.0,
                    'match_streak_count': 0,
                    'listerners': {},
                    'block_states' : {},
                    'block_count' : 0,
                    'block_behavior' : None,
                    'movable_blocks' : {},
                    'match_list' : [],
                    'match_streak_list': [],
                }
            }
        data = self.__globDict['play_session']
        self.moves = data['moves']
        self.time = data['time']
        self.streakCount = data['match_streak_count']
        self.listerners = data['listerners']
        self.blockStates = data['block_states']
        self.blockCount = data['block_count']
        self.blockBehavior = data['block_behavior']
        self.movableBlocks = data['movable_blocks']
        self.matchList = data['match_list']
        self.matchStreakList = data['match_streak_list']
    
    def getMatchCount(self):
        return len(self.matchList)

class PlayerGlobalData(GlobDict):
    def __init__(self):
        self.GlobDict.__init__(self)
        if 'player' not in self.__globDict:
            self.__globDict['player'] = {
                'id' : '',
                'name' : ''
            }
        data = self.__globDict['player']
        self.id = data['id']
        self.name = data['name']

class LoadedChallengeGlobalData(GlobDict):
    def __init__(self):
        self.GlobDict.__init__(self)
        if 'loaded_challenge' not in self.__globDict:
            self.__globDict['loaded_challenge'] = {
                'name' : '', 'pattern' : '',
                'behavior' : '','instructions': ''
            }
        
        self.__data = self.__globDict['active_challenge']
        self.name = data['name']
        self.pattern = data['pattern']
        self.behavior = data['behavior']
        self.instructions = data['instructions']
    
    def getChallenge(self):
        return self.__data

    def getPattern(self):
        if self.name in PUZZLE_PATTERNS_4X4:
            return PUZZLE_PATTERNS_4X4[self.name]
        return {}

    def getBehavior(self):
        if self.behavior in BLOCK_BEHAVIORS:
            return BLOCK_BEHAVIORS[self.behavior]
        return {}

    def getId(self):
        name = self.name.replace(' ','_'),
        return '%s_%s_%s' % (name, self.pattern, self.behavior)

    def set(self, challengeDict):
        self.__data = challengeDict