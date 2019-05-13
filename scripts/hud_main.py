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
from listerner import Listerner
from game_event_listerners import OnGameStartListerner, OnGameStopListerner
from hud_listerners import HudClockListerner
from challenge_viewer_main import startChallengeViewerScene

log = logger()

def init(controller):
    own = controller.owner
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStopListerner().attach('stop_clock', Clock(own).stop)
    HudClockListerner().attach('update_hud_clock', updateHudTimer)
    OnloadHudListerner().onload()

def startHudScene():
    overlayHud()

def displayHud():
    from game import reshuffle, pause, quit
    canvas = HudCanvas()
    canvas.loadStatic()

    pauseBtn = Button(canvas.pauseBtnObj, logic)
    homeBtn = Button(canvas.homeBtnObj, logic)
    shuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    patternBtn = Button(canvas.patternBtnObj, logic)
    
    patternBtn.setOnclickAction(
        lambda: startChallengeViewerScene()
    )
    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.setOnclickAction(pause)
    homeBtn.setOnclickAction(quit)
    canvas.show(canvas.canvasObj)

def updateHudTimer(curTime):
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.clockTxtObj, frmtTime(curTime))

def runTimer(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')

    if isActive:
        HudClockListerner().update(var.getProp('timer'))

def showMoves(controller):
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.movesTxtObj, getPlayStats('moves'))

class HudClock(Clock):
    def __init__(self):
        loadMain('HUD')
        super(Clock, self).__init__()
        shelper = SceneHelper(logic)
        scene = shelper.getscene('HUD')
        timerObj = scene.objects['hud_main']
        Clock.__init__(self, timerObj)


