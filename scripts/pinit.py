#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: This module is an entry point to the puzzle
#               game. States can be specified here and 
#               the solve pattern too..
#########################################################
from navigator import overlayHud
from loader import add_loading_screen
from puzzle import PuzzleLoader
from bge import logic
from game import getPuzzleState, createSession

@add_loading_screen
def init():
    overlayHud()
    createSession()
    initPuzzleBoard(getPuzzleState('block_pattern'))
    return True    

def initPuzzleBoard(pattern):
    puzzle = PuzzleLoader(logic.getCurrentScene())
    puzzle.setStaticBlockNumbers(pattern)
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()