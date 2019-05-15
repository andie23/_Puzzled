from listerner import Listerner
from logger import logger

log = logger()

class GameListerner(Listerner):
    def __init__(self, channel):
        from session_listerner_global_data import SessionListernerData
        super(GameListerner, self).__init__(SessionListernerData(channel))

class OnGamePauseListerner(GameListerner):
    def __init__(self):
        super(OnGamePauseListerner, self).__init__('ON_GAME_PAUSE')

    def onPause(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameResumeListerner(GameListerner):
    def __init__(self):
        super(OnGameResumeListerner, self).__init__('ON_GAME_RESUME')
    
    def onResume(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleCompleteListerner(GameListerner):
    def __init__(self):
        super(OnPuzzleCompleteListerner, self).__init__('ON_PUZZLE_COMPLETE')
    
    def onComplete(self):
        self.updateListerners(lambda listerner: listerner())

class OnGameStopListerner(GameListerner):
    def __init__(self):
        super(OnGameStopListerner, self).__init__('ON_GAME_STOP')

    def onStop(self):
        log.debug('Running on quit listerners %s', self.getListerners())
        self.updateListerners(lambda listerner: listerner())

class OnGameStartListerner(GameListerner):
    def __init__(self):
        super(OnGameStartListerner, self).__init__('ON_GAME_START')

    def onStart(self):
        log.debug('Running onstart listerners %s', self.getListerners())
        self.updateListerners(lambda listerner: listerner())

class OnInvokePuzzleReshuffleListerner(GameListerner):
    def __init__(self):
        super(OnInvokePuzzleReshuffleListerner, self).__init__('ON_PUZZLE_RESHUFFLE')

    def onInvoke(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleRestartListerner(GameListerner):
    def __init__(self):
        super(OnPuzzleRestartListerner, self).__init__('ON_PUZZLE_RESTART')
    
    def onRestart(self):
        self.updateListerners(lambda listerner: listerner())

class OnInvokeGameQuitListerner(GameListerner):
    def __init__(self):
        super(OnInvokeGameQuitListerner, self).__init__('ON_GAME_QUIT')
    
    def onInvoke(self):
        self.updateListerners(lambda listerner: listerner())

class OnPuzzleExitListerner(GameListerner):
    def __init__(self):
        super(OnPuzzleExitListerner, self).__init__('ON_EXIT')
    
    def onExit(self):
        self.updateListerners(lambda listerner: listerner())
