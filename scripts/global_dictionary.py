from bge import logic

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

class PlayerGlobalData(GlobDict):
    def __init__(self):
        self.GlobDict.__init__(self)
        if 'player' not in self.__globDict:
            self.__globDict['player'] = {
                'id' : 'default',
                'name' : 'default'
            }
        data = self.__globDict['player']
        self.id = data['id']
        self.name = data['name']

class LoadedChallengeGlobalData(GlobDict):
    def __init__(self):
        self.GlobDict.__init__(self)
        if 'loaded_challenge' not in self.__globDict:
            self.__globDict['loaded_challenge'] = {
                'name' : 'unknown',
                'pattern' : 'unknown',
                'behavior' : 'unknown',
                'instructions': 'none'
            }
        
        data = self.__globDict['active_challenge']
        self.name = data['name']
        self.pattern = data['pattern']
        self.behavior = data['behavior']
        self.instructions = data['instructions']
