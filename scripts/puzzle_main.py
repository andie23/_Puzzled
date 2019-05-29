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
    # Reset session if data from a previous session exists
    session = SessionGlobalData(reset=True)
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
        'enable_space_block', lambda: SpaceBlock(scene).enable()
    )
    
    OnGameStopListerner().attach(
        'disable_space_block', lambda: SpaceBlock(scene).disable()
    )

    OnPuzzleCompleteListerner().attach(
        'stop_game', stop
    )

    OnPuzzleCompleteListerner().attach(
        'show_assessment', showAssessment
    )

    OnInvokeGameQuitListerner().attach(
        'confirm_exit', onQuit
    )

    OnInvokePuzzleReshuffleListerner().attach(
        'confirm_reshuffle', onReshuffle
    )


@confirm('Exit', 'Really? are you sure you want to quit now?')   
def onQuit():
    from game_event_listerners import OnPuzzleExitListerner

    OnPuzzleExitListerner().onExit()
    startChallengeListScene()

@confirm('Reshuffle', 'Really? do you want to reshuffle?')
def onReshuffle():
    from game_event_listerners import OnPuzzleRestartListerner
    from navigator import SceneHelper
    from session_global_data import SessionGlobalData

    OnPuzzleRestartListerner().onRestart()
    SceneHelper(logic).restart(['MAIN'])

def checkMatchList(session):
    if session.getMatchCount() >= session.getBlockCount():
        OnPuzzleCompleteListerner().onComplete()

def showAssessment():
    from notification import showNotification
    from timer import Timer
    from player import getPlayerName

    showNotification('Congraturations %s !!' % getPlayerName(), duration=5.0)
    timer = Timer('assessment_preview', 'MAIN')
    timer.setTimer(6.0, overlayAssessment)
    timer.start()

def initPuzzleBoard(pattern):
    from puzzle_loader import PuzzleLoader

    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    return len(puzzle.getVisualBlocks())


    
