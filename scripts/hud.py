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
from game import reshuffle, pause

log = logger()

def init():
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

    Text(canvas.titleTxtObj, title, 10)
    if score.isset():
        Text(canvas.prevTimeTxtObj, frmtTime(score.timeCompleted))
        Text(canvas.prevMovesTxtObj, score.moves)
    else:
        Text(canvas.prevTimeTxtObj, '00:00:00')
        Text(canvas.prevMovesTxtObj, '0')

    pauseBtn = Button(canvas.pauseBtnObj, logic)
    homeBtn = Button(canvas.homeBtnObj, logic)
    shuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    patternBtn = Button(canvas.patternBtnObj, logic)
    
    patternBtn.setOnclickAction(overlayPattern, logic.globalDict['gsetup'])
    shuffleBtn.setOnclickAction(reshuffle)
    pauseBtn.setOnclickAction(pause)
    homeBtn.setOnclickAction(navToChallenges)

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
    gdict = logic.globalDict
    own = controller.owner
    moves = gdict['NumberOfMoves']
    canvas = HudCanvas(logic)
    canvas.load('Hud')
    Text(canvas.movesTxtObj, moves)


class Clock():
    def __init__(self, logic, sceneID=1, timerObj=None):
        if sceneID:
            self.scene = logic.getSceneList()[sceneID]
        else:
            self.scene = logic.getCurrentScene()
        
        if timerObj:
            self.timerObj = ObjProperties(timerObj)
        else:
            self.timerObj = ObjProperties(self.scene.objects['hud_main'])

    def start(self):
        if not self.isActive:
            self.timerObj.setProp('is_timer_active', True)
            log.debug('Timer has started')

    def stop(self):
        if self.isActive:
            self.snaptimer()
            self.timerObj.setProp('is_timer_active', False)
            log.debug('Timer is stopped')

    def reset(self):
        self.timerObj.setProp('timer', 0.0)
        self.snaptimer()
        log.debug('Timer has been reset.')
    
    def resume(self):
        if not self.isActive:
            self.settimer(self.snapshot)
            self.start()
            log.debug('Resuming timer from "%s"', self.snapshot)

    def curtime(self):
        return self.timerObj.getProp('timer')

    @property
    def isActive(self):
        return self.timerObj.getProp('is_timer_active')

    @property
    def snapshot(self):
        return self.timerObj.getProp('timer_snapshot')
    
    def snaptimer(self):
        timer = self.timerObj.getProp('timer')
        self.timerObj.setProp('timer_snapshot', timer)
        log.debug('Timer snapshot "%s" has been captured', timer)

    def settimer(self, val):
        self.timerObj.setProp('timer', val)
