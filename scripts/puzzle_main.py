from bge import logic
from game_event_listerners import *
from navigator import *
from loader import add_loading_screen
from dialog import confirm, infoDialog
from block_listerners import *
from match_update import *

def init():
    from notification import showNotification
    from sblock import SpaceBlock
    from game import start, stop
    from session_global_data import SessionGlobalData
    from challenge_global_data import LoadedChallengeGlobalData
    from hud_listerners import OnloadHudListerner
    from hud_listerners import OnOpenDialogListerner, OnCloseDialogListerner
    from hud_resources import loadInGameHud
    
    scene = Scene('MAIN')
    session = SessionGlobalData(reset=True)
    loadedChallenge = LoadedChallengeGlobalData()
    blockBehavior = loadedChallenge.getBehavior()
    blockCount = initPuzzleBoard(scene, loadedChallenge.getPattern())
    spaceBlock = SpaceBlock()
    session.setBlockCount(blockCount)
    
    OnBlockInitListerner().attach(
        'set_block_behavior', lambda b: blockBehavior()
    )

    OnBlockInitListerner().attach(
        'initialise_match_evaluation', lambda block: evaluateMatch(block)
    )

    OnMatchListerner().attach(
        'increment_match_count', lambda b: session.incrementMatchCount()
    )
    
    OnMatchListerner().attach(
        'build_match_streak', lambda b: buildStreakCount(session)
    )
    
    OnMatchListerner().attach(
        'check_match_count', lambda b: checkMatchCount(session)
    )

    OnMisMatchListerner().attach(
        'decrement_match_count', lambda b, wasMatch: decrementMatchCount(session, wasMatch)
    )
    
    OnMisMatchListerner().attach(
        'reset_match_streak', lambda b, w: resetMatchstreak(session)
    )

    OnBlockMovementStartListerner().attach(
        'clear_movable_blocks', lambda b: session.clearMovableBlocks()
    )

    OnBlockMovementStartListerner().attach(
        'increment_moves', lambda b: session.incrementMoves()
    )

    OnBlockMovementStopListerner().attach(
        'match_position_node_id_to_block_id', lambda block: evaluateMatch(block) 
    )

    OnBlockMovementStopListerner().attach(
        'detect_logical_blocks', lambda b: detectLogicalBlocks(
            OnDetectLogicalBlocksListerner(), spaceBlock
        )
    )

    OnDetectLogicalBlocksListerner().attach(
        'set_movable_blocks_in_session', lambda m: session.setMovableBlocks(m)
    )

    OnDetectLogicalBlocksListerner().attach(
        'unlock_space_block', lambda m: spaceBlock.unLock()
    )

    OnGameStartListerner().attach(
        'detect_initial_logical_blocks', lambda: detectLogicalBlocks(
            OnDetectLogicalBlocksListerner(), spaceBlock
        )
    )

    OnOpenDialogListerner().attach(
        'disable_spaceblock', spaceBlock.disable
    )

    OnCloseDialogListerner().attach(
        'enable_spaceblock', spaceBlock.enable
    )

    OnGameStartListerner().attach(
        'enable_space_block', spaceBlock.enable
    )
    
    OnGameStopListerner().attach(
        'disable_space_block', spaceBlock.disable
    )

    OnPuzzleCompleteListerner().attach(
        'stop_game', stop
    )

    OnPuzzleRestartListerner().attach(
        'restart_puzzle_scene', scene.restart
    )
    
    OnPuzzleRestartListerner().attach(
        'show_notification', lambda: showNotification('Puzzle has been reshuffled!')
    )
    
    OnPuzzleExitListerner().attach(
        'go_to_challenges_menu', startChallengeListScene
    )

    OnPuzzleCompleteListerner().attach(
        'evaluate_final_match_streak', lambda: evaluateMatchStreak(session)
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

    OnloadHudListerner().attach(
        'start_game', start
    )

    loadInGameHud()

@confirm('Exit', 'Really? are you sure you want to quit now?')   
def onQuit():
    from game_event_listerners import OnPuzzleExitListerner

    OnPuzzleExitListerner().onExit()

@confirm('Reshuffle', 'Really? do you want to reshuffle?')
def onReshuffle():
    from game_event_listerners import OnPuzzleRestartListerner
    from session_global_data import SessionGlobalData

    OnPuzzleRestartListerner().onRestart()

def initPuzzleBoard(scene, pattern):
    from puzzle_loader import PuzzleLoader

    puzzle = PuzzleLoader(scene.getscene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    return len(puzzle.getVisualBlocks())


    
