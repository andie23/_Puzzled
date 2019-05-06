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
from bootstrap import loadMain

log = logger()
CLOCK_OBSERVERS = 'hud_clock_observers'

def init():
    canvas = HudCanvas()
    canvas.loadStatic()
    setBtnActions(canvas)
    canvas.show(canvas.canvasObj)
    HudClockListerner().attach('hud_timer_updater', updateHudTimer)

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

def updateHudTimer(curTime):
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.clockTxtObj, frmtTime(curTime))

def runTimer(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')
    timerListerners = HudClockListerner().getListerners()

    if isActive:
        for id, listerner in timerListerners.items():
            listerner(var.getProp('timer'))
   
def showMoves(controller):
    from game import getPlayStats
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.movesTxtObj, getPlayStats('moves'))

class HudClockListerner():
    def __init__(self):
        self.gdict = logic.globalDict

    def getListerners(self):
        if CLOCK_OBSERVERS not in self.gdict:
            self.gdict[CLOCK_OBSERVERS] = {}
        return self.gdict[CLOCK_OBSERVERS]

    def attach(self, id, action):
        listerners = self.getListerners()
        if id not in listerners:
            listerners[id] = action
            log.debug('Attached observer %s in %s', id, CLOCK_OBSERVERS)

    def detach(self, id):
        listerners = self.getListerners()
        if id in listerners:
            del listerners[id]
            log.debug('Dettached observer %s in %s', id, CLOCK_OBSERVERS)
    
class HudClock(Clock):
    def __init__(self):
        loadMain('HUD')
        super(Clock, self).__init__()
        shelper = SceneHelper(logic)
        scene = shelper.getscene('HUD')
        timerObj = scene.objects['hud_main']
        Clock.__init__(self, timerObj)


