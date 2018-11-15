#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: This module is an entry point to the puzzle
#               game. States can be specified here and 
#               the solve pattern too..
#########################################################
import navigator
from puzzle import PuzzleLoader
from block import SpaceBlock
from bge import logic
from objproperties import ObjProperties
from logger import logger
from patterns import PUZZLE_PATTERNS_4X4
from sscripts import SCRIPTS
from challenges import CHALLENGE_LIST
from pcache import *
from hud import HudClock
from utils import frmtTime

def main(controller):
    scene = logic.getCurrentScene()
    setup = _getSetup()
    pattern = setup['pattern']
    initPuzzleBoard(scene, pattern)
    initGameProperties(scene, setup)
    navigator.overlayHud()

def start(controller):
    scene = logic.getCurrentScene()
    spaceblock = SpaceBlock(scene)
    clock = HudClock()
    spaceblock.unLock()
    clock.start()

def initProfile():
    profile = Profile(pname='DEFAULT')
    
    if not profile.isNameExists():
        profile.add() 

    logic.globalDict['player'] = {
        'id' : profile.userid,
        'name': profile.username
    }

def initPuzzleBoard(scene, pattern):
    puzzle = PuzzleLoader(scene)
    puzzle.setStaticBlockNumbers(PUZZLE_PATTERNS_4X4[pattern])
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()

def initGameProperties(scene, setup):
    globDict = logic.globalDict
    puzzle = PuzzleLoader(scene)
    eventscript = setup['eventScript']
    globDict['session'] = {
        'moves' : 0,
        'time' : 0.0,
        'chain_count' : 0,
        'input': ''
    }
    globDict['MatchChainList'] = []
    globDict['GameSetup'] = setup
    globDict['GameStatus'] = ''
    globDict['MatchingBlocks'] = []
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1
    globDict['eventScript'] = SCRIPTS[eventscript]

def _getSetup():
    if 'gsetup' not in logic.globalDict:
        gsetup = CHALLENGE_LIST[0]
    else:
        gsetup = logic.globalDict['gsetup']
    gsetup['id'] = '%s_%s' % (gsetup['pattern'], gsetup['eventScript'])
    return gsetup