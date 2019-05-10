from bge import logic

SESSION_DICT = {
    'player': {'name' : ''},
    'challenge' : {'id' : '', 'name' : ''},
    'puzzle' : {
        'listerners': {},
        'block_states' : {},
        'block_count' : 0,
        'block_behavior' : None,
        'block_pattern' : [],
        'movable_blocks' : {},
        'match_list' : [],
        'match_streak_list': [],
    },
    'play' : {
        'moves' : 0,
        'time' : 0.0,
        'match_streak' : 0
    }
}

class GlobDict():
    def __init__(self):
        self.__globDict = logic.globalDict

class ChallengeViewGlobDictData(GlobDict):
    def __init__(self):
        self.sceneRequestedFrom = self.__get('from_scene')
        self.challenge = self.__get('challenge')

    def __get(self, var):
        if 'active_challenge_view' not in self.__globDict:
            return
        
        if not 'active_challenge_view' in self.__globDict:
            return
        
        return self.__globDict['active_challenge_view'][var]

    def create(self, scene, challenge):
        self.__globDict['active_challenge_view'] = {
            'from_scene' : scene,
            'challenge' : challenge
        }

class ActiveChallengeGlobDictData(GlobDict):
    def __init__(self):
        self.__challenge = {}
        self.name = self.__get('name')
        self.behavior = self.__get('behavior')
        self.pattern = self.__get('pattern')

    def __get(self, var):
        if 'loaded_challenge' not in self.__globDict:
            return

        if not self.__globDict['loaded_challenge']:
            return
    
        return self.__globDict['loaded_challenge'][var]

    def create(self, challenge):
        self.__globDict['loaded_challenge'] = challenge

class SessionGlobDict(GlobDict)
    def __init__(self, key):
        GlobDict.__init__(self)
        self.__globDict = logic.globalDict
        self.__data = self.__globDict[key]

        if not self.__isset():
            self.__init()
    
    def __init(self):
        self.__globDict['session'] = SESSION_DICT

    def __isset(self):
        return 'session' in self.__globDict

class PlayerGlobDictData(SessionGlobDict):
    def __init__(self):
        GlobDict.__init__(self, 'player'):
        self.name = self.__data['name']

class ChallengeGlobDictData(SessionGlobDict):
    def __init__(self):
        GlobDict.__init__(self, 'challenge')
        self.id = self.__data['id']
        self.name = self.__data['name']

class PuzzleEnvGlobalDictData(SessionGlobDict):
    def __init__(self):
        GlobDict.__init__(self, 'puzzle_env')
        self.listerners = self.__data['listerners']
        self.blockStates = self.__data['block_states']
        self.blockCount = self.__data['block_count']
        self.blockBehavior = self.__data['block_behavior']
        self.blockPattern = self.__data['block_pattern']
        self.movableBlocks = self.__data['movable_blocks']
        self.matchList = self.__data['match_list']
        self.matchStreak = self.__data['match_streak']
