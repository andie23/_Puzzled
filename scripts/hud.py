#################################################
# Author: Andrew Mfune
# Date: 04/07/2018
# Description: All HUD objects have they're 
#              logic resides here.
#################################################
from bge import logic
from canvas import HudCanvas
from widgets import Text, Button
from objproperties import ObjProperties
from utils import frmtTime
from logger import logger
from pcache import Scores
from navigator import *
from clock import Clock

def init():
    from game import reshuffle, pause, quit

    shelper = SceneHelper(logic)
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']
    title = gsetup['name']
    canvas = HudCanvas(logic)
    canvas.load('Hud')
    score = Scores(pid=playerID, challenge=challenge)

    if score.isset():
        Text(canvas.prevTimeTxtObj, frmtTime(score.timeCompleted))
        Text(canvas.prevMovesTxtObj, score.moves)
    else:
        Text(canvas.prevTimeTxtObj, 'No Record')
        Text(canvas.prevMovesTxtObj, 'No Record')

    pauseBtn = Button(canvas.pauseBtnObj, logic)
    homeBtn = Button(canvas.homeBtnObj, logic)
    shuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    patternBtn = Button(canvas.patternBtnObj, logic)
    
    patternBtn.setOnclickAction(overlayPattern, logic.globalDict['gsetup'])
    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.setOnclickAction(pause)
    homeBtn.setOnclickAction(quit)
    canvas.fadeIn()

def showTime(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')

    if isActive:
        canvas = HudCanvas(logic)
        canvas.load('Hud')
        curTime = var.getProp('timer')
        Text(canvas.clockTxtObj, frmtTime(curTime))

def showMoves(controller):
    from game import getSessionVar
    own = controller.owner
    moves = getSessionVar('moves')
    canvas = HudCanvas(logic)
    canvas.load('Hud')
    Text(canvas.movesTxtObj, moves)


class HudClock(Clock):
    def __init__(self):
        super(Clock, self).__init__()
        shelper = SceneHelper(logic)
        scene = shelper.getscene('HUD')
        timerObj = scene.objects['hud_main']
        Clock.__init__(self, timerObj)

