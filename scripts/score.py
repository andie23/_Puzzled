from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from hudapi import HUD_Clock, HUD_CachedTime, HUD_CurrentTime
from utils import *

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
            clock = HUD_Clock()
            clock.stop()
            spaceBlock.lock()
            gstatus['isActive'] = False
            _updateScore(clock.snapshot)

def _updateScore(finishTime):
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']

    hudClock = HUD_Clock()
    hudCachedTime = HUD_CachedTime()
    hudCurTim = HUD_CurrentTime()

    score = Scores(pid=playerID, challenge=challenge)

   
    if not score.isset():
        hudClock.settxt('You Win!!', lock=True, right=25)
        hudCachedTime.setheadertxt('Initial Record:', left=10)
        hudCachedTime.settxt(frmtTime(finishTime))
        hudCachedTime.show()
        hudCachedTime.showHeader()
        score.add(finishTime)
        return

    prevtime = score.timeCompleted
    
    if finishTime < prevtime:
        percDiff = calcPercDiff(prevtime, finishTime)
        assessmentTxt = 'Assessment: {0}% Better!!'.format(percDiff)
        hudClock.settxt(assessmentTxt, lock=True, right=33)
        score.editTime(finishTime)
    else:
        percDiff = calcPercDiff(finishTime, prevtime)
        assessmentTxt = 'Assessment: {0}% Worse!!'.format(percDiff)
        hudClock.settxt(assessmentTxt, lock=True, right=33)

    hudCachedTime.setheadertxt('Previous - Current:')
    hudCachedTime.settxt('%s - %s' % (
        frmtTime(prevtime), 
        frmtTime(finishTime)
    ))
    
    hudCurTim.setheadertxt('Number of Moves:')
    hudCurTim.settxt(gdict['NumberOfMoves'])
    hudCurTim.show()
    hudCurTim.showHeader()