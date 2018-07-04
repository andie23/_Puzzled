###############################################################
# Author: Andrew Mfune
# Date: 04/07/2018
# Description: This module has API modules for manipulating 
#              Objects in the HUD scene i.e. The clock can
#              be given instructions to stop, start or reset 
#              by other objects    
###############################################################
from objproperties import ObjProperties
from bge import logic
from logger import logger

log = logger()

class HudObjs:
    def __init__(self):
        self.scenes = logic.getSceneList()
        self.hudscene = self.scenes[1]
        self.hudobjs = self.hudscene.objects

    def gettimerObj(self):
        return self.hudobjs['timerObj']
    
    def getPrevTimeObj(self):
        return self.hudobjs['prevTime']

class PrevTimeTxt(HudObjs):
    def __init__(self):
        super(HudObjs, self).__init__()
        HudObjs.__init__(self) 
        self.txtObj = self.getPrevTimeObj()
        self.txtProps = ObjProperties(self.txtObj)
    
    def show(self):
        self.txtObj.setVisible(True)

    def hide(self):
        self.txtObj.setVisible(False)

    def settxt(self, txt):
        self.txtProps.setProp('Text', txt)

class Clock(HudObjs):
    def __init__(self):
        super(HudObjs, self).__init__()
        HudObjs.__init__(self)
        self.timerObj = self.gettimerObj()
        self.timerProps = ObjProperties(self.timerObj)

    def start(self):
        if not self.isActive:
            self.timerProps.setProp('is_active', True)
            log.debug('Timer started')

    def stop(self):
        if self.isActive:
            self.snaptimer()
            self.timerProps.setProp('is_active', False)
            log.debug('Timer stopped')

    def reset(self):
        self.timerObj.setProp('timer', 0.0)
        self.snaptimer()
        log.debug('Timer has been reset.')
    
    def resume(self):
        if not self.isActive:
            self.settimer(self.snapshot)
            self.start()
            log.debug('Resuming timer with snapshot "%s"', self.snapshot)

    def curtime(self):
        return self.timerObj.getProp('timer')

    def show(self):
        self.timerObj.setVisible(True)
        self.timerProps.setProp('is_visible', True)
        log.debug('Timer is now visible')

    def hide(self):
        self.timerObj.setVisible(False)
        self.timerProps.setProp('is_visible', False)
        log.debug('Timer is now hidden')

    @property
    def isActive(self):
        return self.timerProps.getProp('is_active')

    @property
    def snapshot(self):
        return self.timerProps.getProp('snapshot')
    
    def snaptimer(self):
        timer = self.timerProps.getProp('timer')
        self.timerProps.setProp('snapshot', timer)
        log.debug('Timer snapshot "%s" has been captured', timer)

    def settimer(self, val):
        self.timerObj.setProp('timer', val)
