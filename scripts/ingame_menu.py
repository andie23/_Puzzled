from bge import logic
from hud_canvas import HudCanvas
from button_widget import Button
from text_widget import Text
from objproperties import ObjProperties
from utils import frmtTime
from clock import Clock

def init(controller):
    from menu import Menu, BACK_POSITION_NODE
    from scene_helper import Scene
    from navigator import closeHudScreen
    from hud_listerners import HudClockListerner, OnloadHudListerner
    from game_event_listerners import OnGameStartListerner
    from game_event_listerners import OnGameStopListerner
    from game_event_listerners import OnPuzzleExitListerner
    from game_event_listerners import OnPuzzleCompleteListerner
    from game_event_listerners import OnPuzzleRestartListerner
    from game_event_listerners import OnGamePauseListerner
    from game_event_listerners import OnGameResumeListerner
    from block_listerners import OnBlockMovementStartListerner
    from session_global_data import SessionGlobalData

    own = controller.owner
    menu = Menu(HudCanvas(), BACK_POSITION_NODE)

    OnBlockMovementStartListerner().attach('update_moves', lambda b: updateMoveCount())
    OnPuzzleRestartListerner().attach('restart_hud', Scene('HUD').restart)
    OnPuzzleExitListerner().attach('restart_hud', Scene('HUD').restart)
    OnPuzzleCompleteListerner().attach('disable_menu', menu.canvas.disable)
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStartListerner().attach('enable_hud', menu.canvas.enable)
    OnGamePauseListerner().attach('pause_clock', Clock(own).stop)
    OnGameResumeListerner().attach('resume_clock', Clock(own).resume)
    OnGameStopListerner().attach('stop_clock', Clock(own).stop)
    HudClockListerner().attach('update_hud_clock', updateHudTimer)
    HudClockListerner().attach('update_session_time', SessionGlobalData().setTime)
    OnloadHudListerner().onload()

def displayHud():
    from hud_resources import loadPuzzlePatternViewer
    from game import reshuffle, pause, quit, resume
    from navigator import overlayChallengeViewer
    from button_widget import Button
    from canvas_effects import fadeIn
    
    canvas = HudCanvas()
    
    pauseBtn = Button(canvas.pauseBtnObj)
    resumeBtn = Button(canvas.resumeBtnObj)
    homeBtn = Button(canvas.homeBtnObj)
    shuffleBtn = Button(canvas.reshuffleBtnObj)
    patternBtn = Button(canvas.patternBtnObj)
    
    patternBtn.setOnclickAction(loadPuzzlePatternViewer)
    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.toggleBtn(resumeBtn, resume, pause)
    homeBtn.setOnclickAction(quit)

def onMouseAction(cont):
    from mscursor import Cursor, HAND_POINTER, FIST_POINTER
    
    own = cont.owner
    msHoverSen = own.sensors['hover']
    msClickSen = own.sensors['click']
    
    handCursor = Cursor(HAND_POINTER)
    
    if msHoverSen.positive and msClickSen.positive:
        Cursor(FIST_POINTER).use()    
    elif msHoverSen.positive:
        handCursor.use()
    else:
        Cursor(handCursor.getDefaultCursor()).use()

def updateHudTimer(curTime):
    '''
    Update timer text object with formated time
    '''

    Text(HudCanvas().clockTxtObj, frmtTime(curTime))

def updateTimerListerners(controller):
    '''
    Get current timer every frame and update listerners
    '''
    from hud_listerners import HudClockListerner

    HudClockListerner().update(
        Clock(controller.owner).curtime()
    )

def updateMoveCount():
    from session_global_data import SessionGlobalData
    Text(HudCanvas().movesTxtObj, SessionGlobalData().getMoves())
