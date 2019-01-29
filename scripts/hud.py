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
    canvas = HudCanvas()
    canvas.loadStatic()
    setScoreDisplay(canvas)
    setBtnActions(canvas)
    canvas.fadeIn()

def setBtnActions(canvas):
    from game import reshuffle, pause, quit

    pauseBtn = Button(canvas.pauseBtnObj, logic)
    homeBtn = Button(canvas.homeBtnObj, logic)
    shuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    patternBtn = Button(canvas.patternBtnObj, logic)
    
    patternBtn.setOnclickAction(
        overlayPattern, getSession('pId'), getSession('chngId'),
        logic.globalDict['loaded_challenge']
    )
    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.setOnclickAction(pause)
    homeBtn.setOnclickAction(quit)

def getSession(var=None):
    from game import getDefaultUser, getActiveChallenge
    data = {
        'pId': getDefaultUser('id'),
        'chngId': getActiveChallenge('id')
    }
    if var:
        return data[var]
    return data

def setScoreDisplay(canvas):
    score = Scores(getSession('pId'), getSession('chngId'))

    if score.fetch():
        Text(canvas.prevTimeTxtObj, frmtTime(score.timeCompleted))
        Text(canvas.prevMovesTxtObj, score.moves)
        Text(canvas.prevStreakTxtObj, score.streaks)
    else:
        Text(canvas.prevTimeTxtObj, 'No Record')
        Text(canvas.prevMovesTxtObj, 'No Record')
        Text(canvas.prevStreakTxtObj, 'No Record')

def showTime(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')

    if isActive:
        curTime = var.getProp('timer')
        canvas = HudCanvas()
        canvas.load()
        Text(canvas.clockTxtObj, frmtTime(curTime))

def showMoves(controller):
    from game import getPlayStats
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.movesTxtObj, getPlayStats('moves'))

class HudClock(Clock):
    def __init__(self):
        super(Clock, self).__init__()
        shelper = SceneHelper(logic)
        scene = shelper.getscene('HUD')
        timerObj = scene.objects['hud_main']
        Clock.__init__(self, timerObj)

