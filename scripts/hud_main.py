from bge import logic
from canvas import HudCanvas
from widgets import Text, Button
from objproperties import ObjProperties
from utils import frmtTime
from clock import Clock
from bootstrap import loadMain

def init(controller):
    from navigator import closeHudScreen
    from hud_listerners import HudClockListerner, OnloadHudListerner
    from game_event_listerners import OnGameStartListerner
    from game_event_listerners import OnGameStopListerner
    from game_event_listerners import OnPuzzleExitListerner
    from block_listerners import OnBlockMovementListerner
    from session_global_data import SessionGlobalData

    own = controller.owner
    OnBlockMovementListerner().attach('update_moves', updateMoveCount)
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStopListerner().attach('stop_clock', Clock(own).stop)
    HudClockListerner().attach('update_hud_clock', updateHudTimer)
    HudClockListerner().attach('update_session_time', SessionGlobalData().setTime)
    OnPuzzleExitListerner().attach('close_hud', closeHudScreen)
    OnloadHudListerner().onload()

def displayHud():
    from game import reshuffle, pause, quit
    from challenge_viewer_main import startChallengeViewerScene

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
    from hud_listerners import HudClockListerner

    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')

    if isActive:
        HudClockListerner().update(var.getProp('timer'))

def updateMoveCount():
    from session_global_data import SessionGlobalData
    canvas = HudCanvas()
    canvas.load()
    Text(canvas.movesTxtObj, SessionGlobalData().getMoves())

class HudClock(Clock):
    def __init__(self):
        loadMain('HUD')
        super(Clock, self).__init__()
        shelper = SceneHelper(logic)
        scene = shelper.getscene('HUD')
        timerObj = scene.objects['hud_main']
        Clock.__init__(self, timerObj)


