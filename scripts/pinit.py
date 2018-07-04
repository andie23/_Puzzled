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
from sscripts import SCRIPTS
from psetup import PSETUPS
from pcache import *
from hudapi import Clock

def main(controller):
    scene = logic.getCurrentScene()
    setup = _getSetup()
    pattern = setup['pattern']
    initPuzzleBoard(scene, pattern)
    initGameProperties(scene, setup)
    initProfile()
    initHud()

def start(controller):
    """ 
    Unlock the spaceblock and start the clock.
    
    Inorder to initialize the clock, the HUD scene must be loaded as an overlay.
    The HUD scene is available in the getSceneList after initialisation in the 
    next logical tick.
    This is why the start module must be attached to an always sensor with pospulsemode
    True. Once The HUD scene with it's objects are available, we can proceed to 
    unlock the spaceblock, start the clock and disable pospulse mode.. 
    """

    alwaysen = controller.sensors['start']
    scenes = logic.getSceneList()

    if len(scenes) > 1:
        clock = Clock()
        spaceblock = SpaceBlock(scenes[0].objects['space_block'])
        spaceblock.unLock()
        clock.start()
        alwaysen.usePosPulseMode = False

def initHud():
    logic.addScene('HUD', 1)

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
    globDict['GameSetup'] = setup
    globDict['GameStatus'] = {'isActive': True, 'finishTime' : 0.0}
    globDict['MatchingBlocks'] = {}
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1
    globDict['eventScript'] = SCRIPTS[eventscript]

def _getSetup():
    gsetup = PSETUPS['DEFAULT']
    gsetup['id'] = '%s_%s' % (gsetup['pattern'], gsetup['eventScript'])
    return gsetup