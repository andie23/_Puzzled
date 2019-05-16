from global_dictionary import GlobDict

class SessionGlobalData(GlobDict):
    def __init__(self, reset = False):
        super(SessionGlobalData, self).__init__('play_session')
        
        if not self.data or reset:
            self.setDefaults()
    
    def setDefaults(self):
        self.data['block_count'] = 0
        self.data['listerners'] = {}
        self.data['moves'] = 0
        self.data['time'] = 0.0
        self.data['match_streak_count'] =0
        self.data['block_states'] = {}
        self.data['block_behavior'] = None
        self.data['movable_blocks'] = {}
        self.data['match_list'] = []
        self.data['match_streak_list'] = []

    def getMoves(self):
        return self.data['moves']
    
    def getTime(self):
        return self.data['time']
    
    def getStreakCount(self):
        return self.data['match_streak_count']
    
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
    
    def getMovableBlocks(self):
        return self.data['movable_blocks']
    
    def getMatchList(self):
        return self.data['match_list']
    
    def getMatchStreakList(self):
        return self.data['match_streak_list']
    
    def setMoves(self, moves):
        self.data['moves'] = moves 
    
    def setTime(self, time):
        self.data['time'] = time 
    
    def setStreakCount(self, count):
        self.data['match_streak_count'] = count
    
    def setBlockState(self, block, state):
        self.data['block_states'][block] = state
    
    def setBlockCount(self, count):
        self.data['block_count'] = count
    
    def setMovableBlock(self, block, direction):
        self.data['movable_blocks'][block] = direction

    def clearMovableBlocks(self):
        self.data['movable_blocks'] = {}

    def setBlockInMatchList(self, block):
        self.data['match_list'].append(block)
    
    def removeBlockFromMatchList(self, block):
        self.data['match_list'].remove(block)

    def setBlockInStreakList(self, block):
        self.data['match_streak_list'].append(block)

    def clearStreakList(self):
        self.data['match_streak_list'].clear()

    def getMatchCount(self):
        return len(self.getMatchList())
