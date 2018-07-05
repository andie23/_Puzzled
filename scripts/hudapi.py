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

class Hud:
    def __init__(self, objName):
        self.scenes = logic.getSceneList()
        self.hudscene = self.scenes[1]
        self.hudobjs = self.hudscene.objects
        self.hudObj = self.hudobjs[objName]
        self.hudObjProp = ObjProperties(self.hudObj)

    def getClockObj(self):
        return self.hudobjs['clockObj']
    
    def getCachedTimeObj(self):
        return self.hudobjs['cachedTimeObj']

    def setheadertxt(self, txt, lock=False, spacing=0):
        parentObj = self.hudObj.parent
        if parentObj:
            if spacing > 0 :
                txtspace = '{:>%s}' % spacing
                txt = txtspace.format(txt)
            header = ObjProperties(parentObj)
            header.setProp('Text', txt)
            self.locktxt(lock)

    def settxt(self, txt, lock=False, spacing=0):
        if spacing > 0 :
            txtspace = '{:>%s}' % spacing
            txt = txtspace.format(txt)
        self.hudObjProp.setProp('Text', txt)
        self.locktxt(lock)

    def locktxt(self, boolval):
        self.hudObjProp.setProp('lock_txt', boolval)

    def showHeader(self):
        parentObj = self.hudObj.parent
        if parentObj:
            parentObj.visible = True
    
    def hideHeader(self):
        parentObj = self.hudObj.parent
        if parentObj:
            parentObj.visible = False

    def show(self):
        self.hudObj.visible = True

    def hide(self):
        self.hudObj.visible = False

    def isvisible(self):
        return self.hudObj.visible

class HUD_CachedTime(Hud):
    def __init__(self):
        super(Hud, self).__init__()
        Hud.__init__(self, 'cachedTimeObj')

class HUD_CurrentTime(Hud):
    def __init__(self):
        super(Hud, self).__init__()
        Hud.__init__(self, 'curTimeObj')

class HUD_Clock(Hud):
    def __init__(self):
        super(Hud, self).__init__()
        Hud.__init__(self, 'clockObj')

    def start(self):
        if not self.isActive:
            self.hudObjProp.setProp('is_active', True)
            log.debug('Timer has started')

    def stop(self):
        if self.isActive:
            self.snaptimer()
            self.hudObjProp.setProp('is_active', False)
            log.debug('Timer is stopped')

    def reset(self):
        self.hudObjProp.setProp('timer', 0.0)
        self.snaptimer()
        log.debug('Timer has been reset.')
    
    def resume(self):
        if not self.isActive:
            self.settimer(self.snapshot)
            self.start()
            log.debug('Resuming timer from "%s"', self.snapshot)

    def curtime(self):
        return self.hudObjProp.getProp('timer')

    @property
    def isActive(self):
        return self.hudObjProp.getProp('is_active')

    @property
    def snapshot(self):
        return self.hudObjProp.getProp('snapshot')
    
    def snaptimer(self):
        timer = self.hudObjProp.getProp('timer')
        self.hudObjProp.setProp('snapshot', timer)
        log.debug('Timer snapshot "%s" has been captured', timer)

    def settimer(self, val):
        self.hudObjProp.setProp('timer', val)
