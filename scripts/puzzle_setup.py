#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: This module is an entry point to the puzzle
#               game. States can be specified here and 
#               the solve pattern too..
#########################################################
from puzzle import PuzzleLoader, SpaceBlock
from bge import logic
from objproperties import ObjProperties
from logger import logger
from patterns import PUZZLE_PATTERNS_4X4

def main(controller):
    own = ObjProperties(controller.owner)
    scene = logic.getCurrentScene()
    puzzle = PuzzleLoader(scene)
    initializeProperties(puzzle)
    puzzle.setStaticBlockNumbers(PUZZLE_PATTERNS_4X4[0])
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    spaceBlock = SpaceBlock(scene.objects['space_block'])
    spaceBlock.unLock()
    

def initializeProperties(puzzle):
    globDict = logic.globalDict
    controller = logic.getCurrentController()
    own = ObjProperties(controller.owner)
    globDict['matchingBlocks'] = {}
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1
    globDict['states'] = {
        'MATCH_STATE' : {
            'onMisMatchActions': {
                'ALERT_STATE': {'expiryActions' : 'NO_COLOR_STATE', 'duration': 10.0}}
        }
    }