from bge import logic
from hud_canvas import HudCanvas
from button_widget import Button
from text_widget import Text
from objproperties import ObjProperties
from utils import frmtTime
from clock import Clock

def init(controller):
    from scene_helper import Scene
    from navigator import closeHudScreen
    from hud_listerners import HudClockListerner, OnloadHudListerner
    from game_event_listerners import OnGameStartListerner
    from game_event_listerners import OnGameStopListerner
    from game_event_listerners import OnPuzzleExitListerner
    from game_event_listerners import OnPuzzleCompleteListerner
    from game_event_listerners import OnPuzzleRestartListerner
    from block_listerners import OnBlockMovementStartListerner
    from session_global_data import SessionGlobalData

    own = controller.owner
    canvas = HudCanvas()
    scene = Scene('HUD')

    if not canvas.isset():
        canvas.add(scene.getscene().objects[
            'menu_position_node'
        ])

    OnBlockMovementStartListerner().attach('update_moves', lambda b: updateMoveCount())
    OnPuzzleRestartListerner().attach('restart_clock', Clock(own).reset)
    OnPuzzleExitListerner().attach('restart_hud', scene.restart)
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStartListerner().attach('enable_hud', canvas.enable)
    OnGameStopListerner().attach('stop_clock', Clock(own).stop)
    HudClockListerner().attach('update_hud_clock', updateHudTimer)
    HudClockListerner().attach('update_session_time', SessionGlobalData().setTime)
    OnloadHudListerner().onload()

def displayHud():
    from hud_resources import loadPuzzlePatternViewer
    from game import reshuffle, pause, quit
    from navigator import overlayChallengeViewer
    from button_widget import Button
    from canvas_effects import fadeIn
    canvas = HudCanvas()

    pauseBtn = Button(canvas.pauseBtnObj)
    homeBtn = Button(canvas.homeBtnObj)
    shuffleBtn = Button(canvas.reshuffleBtnObj)
    patternBtn = Button(canvas.patternBtnObj)
    
    patternBtn.setOnclickAction(loadPuzzlePatternViewer)

    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.setOnclickAction(pause)
    homeBtn.setOnclickAction(quit)
    fadeIn(canvas)

def updateHudTimer(curTime):
    Text(HudCanvas().clockTxtObj, frmtTime(curTime))

def runTimer(controller):
    from hud_listerners import HudClockListerner

    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_timer_active')

    if isActive:
        HudClockListerner().update(var.getProp('timer'))

def updateMoveCount():
    from session_global_data import SessionGlobalData
    Text(HudCanvas().movesTxtObj, SessionGlobalData().getMoves())
