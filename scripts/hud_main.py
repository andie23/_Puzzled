from bge import logic
from canvas import HudCanvas
from button_widget import Button
from text_widget import Text
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
    from game_event_listerners import OnPuzzleCompleteListerner
    from game_event_listerners import OnPuzzleRestartListerner
    from block_listerners import OnBlockMovementListerner
    from session_global_data import SessionGlobalData

    own = controller.owner
    OnBlockMovementListerner().attach('update_moves', updateMoveCount)
    OnPuzzleRestartListerner().attach('restart_hud', restartHud)
    OnPuzzleCompleteListerner().attach('close_hud', hideHud)
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStopListerner().attach('stop_clock', Clock(own).stop)
    HudClockListerner().attach('update_hud_clock', updateHudTimer)
    HudClockListerner().attach('update_session_time', SessionGlobalData().setTime)
    OnPuzzleExitListerner().attach('close_hud', closeHudScreen)
    OnloadHudListerner().onload()

def restartHud():
    from navigator import SceneHelper
    SceneHelper(logic).restart(['HUD'])

def hideHud():
    canvas = HudCanvas()
    canvas.load()
    canvas.hide()

def displayHud():
    from game import reshuffle, pause, quit
    from navigator import overlayChallengeViewer
    from button_widget import Button

    canvas = HudCanvas()
    canvas.loadStatic()

    pauseBtn = Button(canvas.pauseBtnObj)
    homeBtn = Button(canvas.homeBtnObj)
    shuffleBtn = Button(canvas.reshuffleBtnObj)
    patternBtn = Button(canvas.patternBtnObj)
    
    patternBtn.setOnclickAction(
        lambda: overlayChallengeViewer()
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


