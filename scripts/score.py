from bge import logic
from puzzle import PuzzleBlockLogic, SpaceBlock
from objproperties import ObjProperties
from pcache import *
from logger import logger
from hudapi import HUD_Clock, HUD_Txt1, HUD_Txt2
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
    moves = gdict['NumberOfMoves']

    hudClock = HUD_Clock()
    hudTxt1 = HUD_Txt1()
    hudTxt2 = HUD_Txt2()

    score = Scores(pid=playerID, challenge=challenge)

    if not score.isset():
        hudClock.settxt('The Puzzle is Puzzled!',right=33)
        hudTxt1.settxtheader('Initial Record:', left=10)
        hudTxt1.settxt(frmtTime(finishTime))
        hudTxt1.show()
        score.add(finishTime, moves)
        return

    prevtime = score.timeCompleted
    prevMoves = score.moves

    if finishTime < prevtime:
        score.editTime(finishTime)
        score.editMoves(moves)
        percDiff = calcPercDiff(prevtime, finishTime)
        assessmentTxt = 'Assessment: {0}% Better!!'.format(percDiff)
        hudClock.settxt(assessmentTxt, right=34)
    else:
        percDiff = calcPercDiff(finishTime, prevtime)
        assessmentTxt = 'Assessment: {0}% Worse!!'.format(percDiff)
        hudClock.settxt(assessmentTxt, right=34)

    hudTxt1.settxtheader('Previous - Current')
    hudTxt1.settxt('%s - %s' % (frmtTime(prevtime), frmtTime(finishTime)))
    
    hudTxt2.settxtheader('Previous - Current', lock=False)
    hudTxt2.settxt('%s - %s' % (prevMoves, moves), lock=True)
