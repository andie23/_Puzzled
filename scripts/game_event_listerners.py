from listerner import Listerner

class OnGamePauseListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_GAME_PAUSE')

    def onPause(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameResumeListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_GAME_RESUME')
    
    def onResume(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleCompleteListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_PUZZLE_COMPLETE')
    
    def onComplete(self):
        self.updateListerners(self, lambda listerner: listerner())

class OnGameStopListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_GAME_STOP')

    def onStop(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameStartListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_GAME_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnInvokePuzzleReshuffleListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_PUZZLE_RESHUFFLE')

    def onReshuffle(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleRestartListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_PUZZLE_RESTART')
    
    def onRestart(self):
        self.updateListerners(lambda listerner: listerner())

class OnInvokeGameQuitListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_GAME_QUIT')
    
    def onQuit(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleExitListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_EXIT')
    
    def onExit(self):
        self.updateListerners(lambda listerner: listerner())
.