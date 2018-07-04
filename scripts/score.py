from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from hudapi import Clock, PrevTimeTxt
from utils import frmtTime
log = logger()

def checkSequence():
    globDict = logic.globalDict
    matchList = globDict['MatchingBlocks']
    matchCount = len(matchList)
    totalBlocks = globDict['totalBlocks']

    if matchCount >= totalBlocks:
        gstatus = globDict['GameStatus']
        if gstatus['isActive']:
            scene = logic.getCurrentScene()
            spaceBlock = SpaceBlock(scene.objects['space_block'])
            clock = Clock()
            clock.stop()
            gstatus['isActive'] = False
            _updateScore(clock.snapshot)
            spaceBlock.lock()

def showPrevScore():
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']
    
    prevTimeTxt = PrevTimeTxt()
    score = Scores(pid=playerID, challenge=challenge)

    if score.isset():
        time = frmtTime(score.timeCompleted)
        prevTimeTxt.settxt(time)
    else:
        prevTimeTxt.hide()

def _updateScore(finishTime):
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']

    score = Scores(pid=playerID, challenge=challenge)

    if not score.isset():
        log.debug('Initial score %s', finishTime)
        score.add(finishTime)
        return

    if finishTime < score.timeCompleted:
        log.debug('New Best finish time! %s', finishTime)
        score.editTime(finishTime)
    
