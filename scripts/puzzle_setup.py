from puzzle import PuzzleLoader
from bge import logic
from objproperties import ObjProperties

DEF_NUM_STRUCT =  {
    1 : [1, 2, 3, 4], 
    2 : [5, 6, 7, 8],
    3 : [9, 10, 11,12],
    4 : [13, 14, 15, 0]
}

def main(controller):
    own = ObjProperties(controller.owner)
    scene = logic.getCurrentScene()
    puzzle = PuzzleLoader(scene)
    initializeProperties(puzzle)
    
    puzzle.setStaticBlockNumbers(DEF_NUM_STRUCT)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    

def initializeProperties(puzzle):
    globDict = logic.globalDict
    controller = logic.getCurrentController()
    own = ObjProperties(controller.owner)
    globDict['matchingBlocks'] = {}
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1