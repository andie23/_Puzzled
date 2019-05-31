from bge import logic
from game_event_listerners import *
from navigator import *
from loader import add_loading_screen
from dialog import confirm, infoDialog
from block_listerners import *
from match_update import *

def init():
    from sblock import SpaceBlock
    from game import start, stop
    from session_global_data import SessionGlobalData
    from challenge_global_data import LoadedChallengeGlobalData
    from hud_listerners import OnloadHudListerner
    
    scene = logic.getCurrentScene()
    session = SessionGlobalData(reset=True)
    loadedChallenge = LoadedChallengeGlobalData()
    blockBehavior = loadedChallenge.getBehavior()
    blockCount = initPuzzleBoard(loadedChallenge.getPattern())
    session.setBlockCount(blockCount)
    overlayHud()

    OnBlockInitListerner().attach(
        'set_block_behavior', lambda b: blockBehavior()
    )

    OnBlockInitListerner().attach(
        'init_match_evaluation', lambda block: evaluateMatch(block)
    )

    # OnMatch order below is important... dont shuffle it around
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
        'increment_moves', lambda b: session.incrementMoves()
    )

    OnBlockMovementStopListerner().attach(
        'match_position_node_id_to_block_id', lambda block: evaluateMatch(block) 
    )

    OnDetectMovableBlocksListerner().attach(
        'unlock_space_block', lambda m: SpaceBlock().unLock()
    )

    OnGameStartListerner().attach(
        'enable_space_block', SpaceBlock().enable
    )
    
    OnGameStopListerner().attach(
        'disable_space_block', SpaceBlock().disable
    )

    OnPuzzleCompleteListerner().attach(
        'stop_game', stop
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


def initPuzzleBoard(pattern):
    from puzzle_loader import PuzzleLoader

    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    return len(puzzle.getVisualBlocks())


    
