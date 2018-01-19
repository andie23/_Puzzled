from puzzle import PuzzleLoader
from bge import logic

DEF_NUM_STRUCT =  {
    1 : [1, 2, 3, 4], 
    2 : [5, 6, 7, 8],
    3 : [9, 10, 11,12],
    4 : [13, 14, 15, 0]
}

def main(controller):
    scene = logic.getCurrentScene()
    puzzle = PuzzleLoader(scene)
    puzzle.setStaticBlockNumbers(DEF_NUM_STRUCT)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()