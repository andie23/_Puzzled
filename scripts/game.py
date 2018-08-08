from bge import logic
from hud import Clock
from puzzle import PuzzleLoader
from block import SpaceBlock

def reshuffle():
    scene = logic.getCurrentScene()
    sblock = SpaceBlock(scene)
    sblock.lock()
    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setLogicalBlockNumbers()
    puzzle.refreshVsBlocks()
    
def reset():
    logic.globalDict['MatchingBlocks'] = []
    logic.globalDict['NumberOfMoves'] = 0
    scene = logic.getCurrentScene()
    sblock = SpaceBlock(scene)
    clock = Clock(logic)
    clock.stop()

    reshuffle()
    sblock.detectNew()

    clock.reset()
    clock.start()
    sblock.unLock()

def stop():
    scene = logic.getCurrentScene()
    sblock = SpaceBlock(scene)
    clock = Clock(logic)

    clock.stop()
    sblock.lock()
