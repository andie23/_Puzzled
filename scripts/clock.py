from objproperties import ObjProperties

class Clock():
    def __init__(self, timerObj):
        self.timerObj = ObjProperties(timerObj)

    def start(self):
        self.timerObj.setProp('is_timer_active', True)
        self.reset()

    def stop(self):
        self.snaptimer()
        self.timerObj.setProp('is_timer_active', False)

    def reset(self):
        self.timerObj.setProp('timer', 0.0)
        self.snaptimer()
    
    def resume(self):
        self.settimer(self.snapshot)
        self.start()

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

    def settimer(self, val):
        self.timerObj.setProp('timer', val)