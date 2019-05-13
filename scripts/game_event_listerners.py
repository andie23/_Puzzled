from listerner import Listerner

class GameListerner(Listerner):
    def __init__(self, channel):
        listernerContainer = PuzzleSessionGlobalData().listerners
        Listerner.__init__(self, listernerContainer, channel)

class OnGamePauseListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_GAME_PAUSE')

    def onPause(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameResumeListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_GAME_RESUME')
    
    def onResume(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleCompleteListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_PUZZLE_COMPLETE')
    
    def onComplete(self):
        self.updateListerners(self, lambda listerner: listerner())

class OnGameStopListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_GAME_STOP')

    def onStop(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameStartListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_GAME_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnInvokePuzzleReshuffleListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_PUZZLE_RESHUFFLE')

    def onReshuffle(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleRestartListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_PUZZLE_RESTART')
    
    def onRestart(self):
        self.updateListerners(lambda listerner: listerner())

class OnInvokeGameQuitListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_GAME_QUIT')
    
    def onQuit(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleExitListerner(GameListerner):
    def __init__(self):
        GameListerner.__init__(self, 'ON_EXIT')
    
    def onExit(self):
        self.updateListerners(lambda listerner: listerner())
.