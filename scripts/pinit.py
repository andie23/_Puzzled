from bge import logic
from game_event_listerners import *
from game import stop
from block import SpaceBlock
from notification import showNotification
from navigator import *
from global_dictionary import *
from player import getPlayer

def init(controller):
    overlayLoadingScreen()
    initPuzzleBoard(getPuzzleState('block_pattern'))
    overlayHud()

    OnGameStartListerner().attach(
        'unlock_space_block', SpaceBlock(scene).unLock
    )
    
    OnGameStartListerner().attach(
        'remove_loading_screen', closeLoadingScreen
    )

    OnGameStopListerner().attach(
        'lock_space_block', SpaceBlock(scene).lock
    )

    OnPuzzleReshuffleListerner().attach(
        'restart_scene', SceneHelper(logic).restart(['MAIN', 'HUD']
    )
    
    OnPuzzleReshuffleListerner().attach(
        'add_loading_screen', overlayLoadingScreen
    )

    OnPuzzleCompleteListerner().attach(
        'stop_game', stop
    )

    OnPuzzleCompleteListerner().attach(
        'show_notification', getNotification
    )

def setSession():
    loadedChallenge = LoadedChallengeGlobDict()
    playerSession = PlayerGlobDict()
    puzzleEnvSession = PuzzleEnvGlobalDict()
    challengeSession = ChallengeGlobDict()

    puzzleEnv.blockPattern = loadedChallenge.challenge
    puzzleEnv.blockBehavior = loadedChallenge.
    

def getNotification():
    showNotification(
        '15 Puzzle Complete..', duration=5.0, callback=overlayAssessment
    )

def initPuzzleBoard(pattern):
    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()