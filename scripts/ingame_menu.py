from bge import logic
from hud_canvas import HudCanvas
from button_widget import Button
from text_widget import Text
from objproperties import ObjProperties
from utils import frmtTime
from clock import Clock
from board_cursor_states import BoardCursorStates

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
    from mscursor import Cursor
    from mscursor import HAND_POINTER, FIST_POINTER, THUMBS_UP_POINTER, THUMBS_DOWN_POINTER

    own = controller.owner
    menu = Menu(HudCanvas(), BACK_POSITION_NODE)
    boardCursorState = BoardCursorStates()
    boardCursorState.setOnHoverCursor(FIST_POINTER)
    boardCursorState.setOnClickCursor(HAND_POINTER)

    OnBlockMovementStartListerner().attach('update_moves', lambda b: updateMoveCount())
    OnPuzzleRestartListerner().attach('restart_hud', Scene('HUD').restart)
    OnPuzzleExitListerner().attach('restart_hud', Scene('HUD').restart)
    OnPuzzleCompleteListerner().attach(
        'change_onhover_board_cursor', lambda: boardCursorState.setOnHoverCursor(THUMBS_UP_POINTER)
    )
    OnPuzzleCompleteListerner().attach(
        'use_thumbs_up_cursor_as_default', Cursor(THUMBS_UP_POINTER).use
    )
    OnPuzzleCompleteListerner().attach('disable_menu', menu.canvas.disable)
    OnGameStartListerner().attach('display_hud', displayHud)
    OnGameStartListerner().attach('start_clock', Clock(own).start)
    OnGameStartListerner().attach('enable_hud', menu.canvas.enable)

    OnGamePauseListerner().attach(
        'override_hand_mouse_cursor', lambda: boardCursorState.setOnHoverCursor(
            THUMBS_DOWN_POINTER
        )
    )
    OnGameResumeListerner().attach(
        'reinstate_hand_mouse_cursor', lambda: boardCursorState.setOnHoverCursor(
            HAND_POINTER
        )
    )
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
    from mscursor import Cursor
    own = cont.owner
    msHoverSen = own.sensors['hover']
    msClickSen = own.sensors['click']
    
    boardCursorState = BoardCursorStates()
    onClickMsCursor = boardCursorState.onClickCursor()
    onHoverMsCursor = boardCursorState.onHoverCursor()
    defaultMsCursor =  Cursor('').getDefaultCursor()
 
    if msHoverSen.positive and msClickSen.positive and onClickMsCursor:
        Cursor(onClickMsCursor).use()    
    elif msHoverSen.positive:
        Cursor(onHoverMsCursor).use()
    else:
        Cursor(defaultMsCursor).use()

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
