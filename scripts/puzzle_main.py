from bge import logic
from game_event_listerners import *
from game import start, stop
from block import SpaceBlock
from notification import showNotification
from navigator import *
from global_dictionary *
from hud_listerners import OnloadHudListerner
from block_listerners import OnMatchListerner
from challenge_menu_view import startChallengeMenuScene
from hud_main import startHudScene
from loader import add_loading_screen

@add_loading_screen
def init(controller):
    loadedChallenge = LoadedChallengeGlobalData()
    blockCount = initPuzzleBoard(loadedChallenge.getPattern())
    createSession(blockCount)
    startHudScene()

    OnloadHudListerner().attach(
        'start_game', start
    )

    OnMatchListerner().attach(
        'check_match_list', checkMatchList
    )
    
    OnGameStartListerner().attach(
        'unlock_space_block', SpaceBlock(scene).unLock
    )
    
    OnGameStartListerner().attach(
        'remove_loading_screen', closeLoadingScreen
    )

    OnGameStopListerner().attach(
        'lock_space_block', SpaceBlock(scene).lock
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

    OnPuzzleRestartListerner().attach(
        'show_loading_screen', overlayLoadingScreen 
    )

@confirm('Exit', 'Really? are you sure you want to quit now?')   
def onQuit():
    startChallengeMenuScene()
    OnPuzzleExistListerner.onExit()

@confirm('Reshuffle', 'Really? do you want to reshuffle?')
def onReshuffle():
    logic.getCurrentScene().restart()
    OnPuzzleRestartListerner.onRestart()

def createSession(blockCount):
    session = PuzzleSessioGlobalData()
    session.blockCount = blockCount

def checkMatchList():
    session = PuzzleSessionGlobalData()
    matchCount = session.getMatchCount()
    totalBlocks = session.blockCount
    
    if (matchCount >= totalBlocks):
        OnPuzzleCompleteListerner().onComplete()

def showAssessment():
    showNotification(
        '15 Puzzle Complete..', duration=5.0, 
        callback=overlayAssessment
    )

def initPuzzleBoard(pattern):
    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    return len(puzzle.getVisualBlocks())

def startPuzzleScene(challenge = None, showInstructions = True):
    loadedChallenge = LoadedChallengeGlobData()
    if challenge is not None:
        loadedChallenge.set(challenge)
    
    if showInstructions and loadedChallenge.instructions:
        overlayDialog()
        return infoDialog(
            title = loadedChallenge.name,
            subtitle = loadedChallenge.instructions
            callback = navToPuzzle
        )
    navToPuzzle()
    
