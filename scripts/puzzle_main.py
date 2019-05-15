from bge import logic
from game_event_listerners import *
from navigator import *
from loader import add_loading_screen
from dialog import confirm, infoDialog

def init():
    from block import SpaceBlock
    from game import start, stop
    from session_global_data import SessionGlobalData
    from challenge_global_data import LoadedChallengeGlobalData
    from hud_listerners import OnloadHudListerner
    from block_listerners import OnMatchListerner

    scene = logic.getCurrentScene()
    session = SessionGlobalData()     
    loadedChallenge = LoadedChallengeGlobalData()
    blockCount = initPuzzleBoard(loadedChallenge.getPattern())
    session.setBlockCount(blockCount)
    overlayHud()

    OnloadHudListerner().attach(
        'start_game', start
    )

    OnMatchListerner().attach(
        'check_match_list', lambda: checkMatchList(session)
    )

    OnGameStartListerner().attach(
        'disable_space_block', lambda: SpaceBlock(scene).enable()
    )
    
    OnGameStopListerner().attach(
        'enable_space_block', lambda: SpaceBlock(scene).disable()
    )

    OnPuzzleCompleteListerner().attach(
        'stop_game', stop
    )

    OnPuzzleCompleteListerner().attach(
        'show_notification', showAssessment
    )

    OnInvokeGameQuitListerner().attach(
        'confirm_exit', onQuit
    )

    OnInvokePuzzleReshuffleListerner().attach(
        'confirm_reshuffle', onReshuffle
    )


@confirm('Exit', 'Really? are you sure you want to quit now?')   
def onQuit():
    OnPuzzleExistListerner.onExit()
    navToChallenges()

@confirm('Reshuffle', 'Really? do you want to reshuffle?')
def onReshuffle():
    OnPuzzleRestartListerner.onRestart()
    logic.getCurrentScene().restart()

def checkMatchList(session):
    if session.getMatchCount() >= session.getBlockCount():
        OnPuzzleCompleteListerner().onComplete()

def showAssessment():
    from notification import showNotification
    showNotification(
        '15 Puzzle Complete..', duration=5.0, 
        callback=overlayAssessment
    )

def initPuzzleBoard(pattern):
    from puzzle_loader import PuzzleLoader

    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    return len(puzzle.getVisualBlocks())


    
