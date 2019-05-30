from global_dictionary import GlobDict

class SessionGlobalData(GlobDict):
    def __init__(self, reset = False):
        super(SessionGlobalData, self).__init__('play_session')
        
        if not self.data or reset:
            self.setDefaults()
    
    def setDefaults(self):
        self.data['block_count'] = 0
        self.data['match_count'] = 0
        self.data['listerners'] = {}
        self.data['top_accumulated_match_streak_count'] = 0
        self.data['accumulated_match_streak_count'] = 0
        self.data['moves'] = 0
        self.data['time'] = 0.0
        self.data['block_states'] = {}
        self.data['block_behavior'] = None
        self.data['movable_blocks'] = {}

    def getMoves(self):
        return self.data['moves']
    
    def getTime(self):
        return self.data['time']
    
    def getAccumulatedMatchStreakCount(self):
        return self.data['accumulated_match_streak_count']

    def getBenchmarkStreakCount(self):
        return self.data['top_accumulated_match_streak_count']
    
    def getListerners(self):
        return self.data['listerners']
    
    def getBlockStates(self):
        return self.data['block_states']
    
    def getBlockState(self, block):
        return self.getBlockStates()[block]

    def getBlockCount(self):
        return self.data['block_count']
    
    def getBlockBehavior(self):
        return self.data['block_behavior']
    
    def getMatchCount(self):
        return self.data['match_count']

    def getMovableBlocks(self):
        return self.data['movable_blocks']
    
    def setMoves(self, moves):
        self.data['moves'] = moves 
    
    def setTime(self, time):
        self.data['time'] = time 
    
    def setStreakCount(self, count):
        self.data['accumulated_match_streak_count'] = count
    
    def setBlockState(self, block, state):
        self.data['block_states'][block] = state
    
    def setBlockCount(self, count):
        self.data['block_count'] = count
    
    def setMovableBlock(self, block, direction):
        self.data['movable_blocks'][block] = direction
    
    def updateMatchStreakBenchmark(self):
        self.data['top_accumulated_match_streak_count'] = self.getAccumulatedMatchStreakCount()
    
    def clearMovableBlocks(self):
        self.data['movable_blocks'] = {}

    def incrementMoves(self):
        self.data['moves'] += 1

    def incrementMatchStreakCount(self):
        self.data['accumulated_match_streak_count'] += 1
    
    def resetMatchStreakCount(self):
        self.data['accumulated_match_streak_count'] = 0

    def incrementMatchCount(self):
        self.data['match_count'] += 1
    
    def decrementMatchCount(self):
        if self.data['match_count'] != 0:
            self.data['match_count'] -= 1

