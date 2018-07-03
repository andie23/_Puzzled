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

def main(controller):
    gsetup = getGameSetup()
    pattern = gsetup['pattern']
    eventScript = gsetup['eventScript']
    own = ObjProperties(controller.owner)
    scene = logic.getCurrentScene()
    puzzle = PuzzleLoader(scene)
    initializeProperties(puzzle, eventScript)
    puzzle.setStaticBlockNumbers(PUZZLE_PATTERNS_4X4[pattern])
    puzzle.addLogicalBlocks()
    puzzle.setLogicalBlockNumbers()
    puzzle.addVisualBlocks()
    spaceBlock = SpaceBlock(scene.objects['space_block'])
    initializeProfile()
    spaceBlock.unLock()

def getGameSetup():
    gsetup = PSETUPS['DEFAULT']
    gsetup['id'] =  '%s_%s' % (gsetup['pattern'], gsetup['eventScript'])
    globDict = logic.globalDict
    globalDict['GameSetup'] = gsetup
    return gsetup

def initializeProperties(puzzle, scriptName):
    globDict = logic.globalDict
    controller = logic.getCurrentController()
    own = ObjProperties(controller.owner)
    globalDict['GameStatus'] = {'isActive': True, 'finishTime' : 0.0}
    globDict['matchingBlocks'] = {}
    globDict['totalBlocks'] = len(puzzle.getStaticBlocks()) -1
    globDict['eventScript'] = SCRIPTS[scriptName]

def initializeProfile():
    profile = Profile()
    
    if not profile.isUsernameExists('DEFAULT'):
        profile.add('DEFAULT')
    
    pid = profile.getID('DEFAULT')
    
    globalDict['player'] = {
        'id' : pid,
        'pname': 'DEFAULT'
    }
