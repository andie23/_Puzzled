###################################
# Author: Andrew Mfune
# Date: 07/06/2018
###################################
from copy import deepcopy
from bge import logic
from logger import logger
from timer import Timer
globalDict = logic.globalDict

log = logger()

class State():
    def __init__(self, block, state):
        self.name = state['action'].__name__
        self.block = block
        self.id = str(block.blockID)
        
        if  'BlockStates' not in globalDict:
            globalDict['BlockStates'] = {}

        if self.id not in globalDict['BlockStates']:
            globalDict['BlockStates'][self.id] = {
                'states' : {},
                'state_anims' : []
            }

        if self.name not in self.states:
            self.setStateInGlobalDict(state)

    @property
    def states(self):
        return globalDict['BlockStates'][self.id]['states']

    @property
    def curState(self):
        return self.states[self.name]
    
    @property
    def hasScope(self):
        return 'scope' in self.curState
        
    @property
    def isBlockInScope(self):
        return self.block.blockID in self.curState['scope']

    @property
    def isDurOrDelSet(self):
        return self.isDelaySet or self.isDurationSet
    
    @property
    def isDurAndDelSet(self):
        return self.isDelaySet and self.isDurationSet

    @property 
    def isDelaySet(self):
        return 'delay' in self.curState

    @property
    def isDurationSet(self):
        return 'duration' in self.curState

    @property 
    def isDelayExp(self):
        if 'isExp' in self.curState['delay']:
            return self.curState['delay']['isExp']
        return False

    @property   
    def isDurationExp(self):
        if 'isExp' in self.curState['duration']:
            return self.curState['duration']['isExp']
        return False

    @property
    def isDurationExpReset(self):
        return self.isPropInState('resetExp', 'duration')
    
    @property
    def isDelayExpReset(self):
        return self.isPropInState('resetExp', 'delay')

    @property
    def isDurationActive(self):
        return self.isTimerSet('duration')

    @property
    def isDelayActive(self):
        return self.isTimerSet('delay')

    @property
    def delayInstanceId(self):
        return 'BID_%s.delay_timer_instance' % self.id
    
    @property
    def durationInstanceId(self):
        return 'BID_%s.duration_timer_instance' % self.id

    @property
    def isDurationTimerReset(self):
        return self.isPropInState('resetTimer', 'duration')

    @property
    def isDelayTimerReset(self):
        return self.isPropInState('resetTimer', 'delay')

    def setDurationExpiry(self, val):
        self.setStateExpiry('duration', val)
   
    def setDelayExpiry(self, val):
        self.setStateExpiry('delay', val)

    def callbackAction(self):
        return self.curState['duration']['callback'](self.block)
  
    def delayAction(self):
        return self.curState['delay']['action'](self.block)

    def setStateExpiry(self, timerType, val):
        self.curState[timerType]['isExp'] = val

    def setStateInGlobalDict(self, state):
        self.states[self.name] = deepcopy(state)

    def cancelDelay(self):
        self.cancelTimer('delay')

    def cancelDuration(self):
        self.cancelTimer('duration')

    def startDelay(self):
        self.startTimer('delay')

    def startDuration(self):
        self.startTimer('duration')

    def startTimer(self, type):
        self.curState[type]['isExp'] = False
        timer = Timer(self.getTimerInstanceId(type), 'MAIN')
        timer.setTimer(self.curState[type]['time'], lambda: self.setStateExpiry(type, True))
        timer.start()

    def runAction(self):
        self.curState['action'](self.block)

    def cancelTimer(self, type):
         timer = Timer(self.getTimerInstanceId(type))
         timer.load()
         timer.destroy()

    def getTimerInstanceId(self, type):
        if type == 'duration':
            return self.durationInstanceId
        elif type == 'delay':
            return self.delayInstanceId

    def isTimerSet(self, type):
        timer = Timer(self.getTimerInstanceId(type), 'MAIN')
        return timer.isAlive()

    def isPropInState(self, prop, type):
        state = self.curState[type]
        if prop in state:
             return state[prop]
        return True
