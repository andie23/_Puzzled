from objproperties import ObjProperties

class Clock():
    '''
    An API for controlling Timer property built 
    into the game engine found in game properties. 
    It provides control for starting, stopping and
    resuming a timer. 

    Note: Game object passed in the constructor must
          have the following properties:
            1) 'timer' type 'Timer'
            2) 'is_timer_active' type 'Boolean'
            3) 'timer_snapshot' type 'Float'
    '''

    def __init__(self, timerObj):
        self.timerObj = ObjProperties(timerObj)

    def start(self):
        self.reset()
        self._setIsActive(True)

    def stop(self):
        self.setTimeSnapshot(self.curtime())
        self._setIsActive(False)

    def reset(self):
        self.settimer(0.0)

    def resume(self):
        self._setIsActive(True)
        self.settimer(self.getTimeSnapshot())

    def curtime(self):
        if not self.isActive:
            return self.getTimeSnapshot()
        return self.timerObj.getProp('timer')

    def setTimeSnapshot(self, time):
        self.timerObj.setProp('timer_snapshot', time)

    def settimer(self, val):
        self.timerObj.setProp('timer', val)

    def _setIsActive(self, bool):
        self.timerObj.setProp('is_timer_active', bool)
    
    def getTimeSnapshot(self):
        return self.timerObj.getProp('timer_snapshot')
 
    @property
    def isActive(self):
        return self.timerObj.getProp('is_timer_active')        