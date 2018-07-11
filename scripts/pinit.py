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
from hudapi import HUD_Clock, HUD_Txt1
from utils import frmtTime

def main(controller):
    scene = logic.getCurrentScene()
    setup = _getSetup()
    pattern = setup['pattern']
    initPuzzleBoard(scene, pattern)
    initGameProperties(scene, setup)
    initProfile()
    initHud()

def start(controller):
    ''' 
    Starts the clock, unlocks the space block and loads data on the HUD...
    
    NOTE: this methord must be executed in the next logic tick.
          Setup a delay sensor attached to this module...
    '''

    scene = logic.getCurrentScene()
    spaceblock = SpaceBlock(scene.objects['space_block'])
    clock = HUD_Clock()
    
    spaceblock.unLock()
    clock.start()
    clock.show()
    _loadHudCachedTime()

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
    globDict['NumberOfMoves'] = 0
    globDict['GameSetup'] = setup
    globDict['GameStatus'] = {'isActive': True, 'finishTime' : 0.0}
    globDict['MatchingBlocks'] = []
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1
    globDict['eventScript'] = SCRIPTS[eventscript]

def _getSetup():
    gsetup = PSETUPS['DEFAULT']
    gsetup['id'] = '%s_%s' % (gsetup['pattern'], gsetup['eventScript'])
    return gsetup

def _loadHudCachedTime():
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']
    
    hudTxt1 = HUD_Txt1()
    score = Scores(pid=playerID, challenge=challenge)
    
    if score.isset():
        time = frmtTime(score.timeCompleted)
        moves = score.moves

        hudTxt1.settxtheader("Benchmark:")
        hudTxt1.settxt('Time: %s - Moves: %s' % (time, moves))
        hudTxt1.show()
    else:
        hudTxt1.hide()