from objproperties import ObjProperties
from logger import logger
log = logger()

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