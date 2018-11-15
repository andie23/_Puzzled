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
        self.name = state['stateObj'].__name__
        self.block = block
        self.id = str(block.blockID)
        
        if  'BlockStates' not in globalDict:
            globalDict['BlockStates'] = {}

        if self.id not in globalDict['BlockStates']:
            globalDict['BlockStates'][self.id] = {'states' : {}}

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
        if 'scope' in self.curState:
            return True
        return False
        
    @property
    def hasCurBlockInScope(self):
        scope = self.curState['scope']

        if self.block.blockID in scope:
            return True

        return False

    @property 
    def isDelaySet(self):
        if 'delay' not in self.curState:
            return False

        delay = self.curState['delay']

        if 'time' not in delay:
            return False

        if delay['time'] <= 0:
            return False
        
        return True

    @property
    def isDurationSet(self):
        if 'duration' not in self.curState:
            return False
            
        duration = self.curState['duration']

        if 'time' not in duration:
            return False

        if duration['time'] <= 0:
            return False

        if 'expiryActions' not in duration:
            return False
    
        return True

    @property
    def isDurationInit(self):
        return self.curState['duration']['isInit']

    @property
    def isDelayInit(self):
        return self.curState['delay']['isInit']

    @property 
    def isDelayExp(self):
        return self.curState['delay']['isExp']
    
    @property   
    def isDurationExp(self):
        return self.curState['duration']['isExp']
    
    @property
    def isDurationInitReset(self):
        return self.isStateProp('resetInit', 'duration')
    
    @property
    def isDelayInitReset(self):
        return self.isStateProp('resetInit', 'delay')

    @property
    def isDurationExpReset(self):
        return self.isStateProp('resetExp', 'duration')
    
    @property
    def isDelayExpReset(self):
        return self.isStateProp('resetExp', 'delay')

    @property
    def isDurationTimerActive(self):
        return self.isTimerActive(self.durationInstanceId, 'duration')

    @property
    def isDelayTimerActive(self):
        return self.isTimerActive(self.delayInstanceId, 'delay')

    @property
    def expiryActions(self):
        return self.curState['duration']['expiryActions']

    @property
    def delayTimerId(self):
        return 'BID_%s.delay_timer_instance' % self.id
    
    @property
    def durationInstanceId(self):
        return 'BID_%s.duration_timer_instance' % self.id

    @property
    def isDurationTimerReset(self):
        return self.isStateProp('resetTimer', 'duration')

    @property
    def isDelayTimerReset(self):
        return self.isStateProp('resetTimer', 'delay')

    def setIsDelayExp(self, val):
        self.curState['delay']['isExp'] = val
        log.debug('%s state %s delay expiry is %s', self.id, self.name, val)
    
    def setIsDurationExp(self, val):
        self.curState['duration']['isExp'] = val
        log.debug('%s state %s duration expiry is %s', self.id, self.name, val)

    def setIsDelayInit(self, val):
        self.curState['delay']['isInit'] = val
    
    def setIsDurationInit(self, val):
        self.curState['duration']['isInit'] = val

    def setStateInGlobalDict(self, state):
        self.states[self.name] = deepcopy(state)

    def cancelDelay(self):
        if self.isDelayTimerActive:
            delay = self.curState['delay']
            timer = Timer(self.delayInstanceId)
            timer.load()
            timer.destroy()
            self.setIsDelayInit(False)

    def cancelDuration(self):
        if self.isDurationTimerActive:
            duration = self.curState['duration']
            timer = Timer(self.durationInstanceId)
            timer.load()
            timer.destroy()
            self.setIsDurationInit(False)

    def startDelay(self):
        delay = self.curState['delay']
        time = delay['time']

        if not 'timer_instance_id' in delay:
            self.setIsDelayInit(False)
            self.setIsDelayExp(False)
    
        if not self.isDelayInit:
            delay['timer_instance_id'] = self.delayInstanceId
            delayTimer = Timer(self.delayInstanceId, 'MAIN')
            delayTimer.setTimer(time, lambda: self.setIsDelayExp(True))
            delayTimer.start()
            self.setIsDelayInit(True)

    def startDuration(self):
        duration = self.curState['duration']
        time = duration['time']

        if not 'timer_instance_id' in duration:
            self.setIsDurationInit(False)
            self.setIsDurationExp(False)
            
        if not self.isDurationInit:
            duration['timer_instance_id'] = self.durationInstanceId
            durationTimer = Timer(self.durationInstanceId, 'MAIN')
            durationTimer.setTimer(time, lambda: self.setIsDurationExp(True))
            durationTimer.start()
            self.setIsDurationInit(True)
    
    def isTimerActive(self, instanceId, timerType):
        timerState = self.curState[timerType]
        if 'timer_instance_id' in timerState:
            instanceId = timerState['timer_instance_id']
            timer = Timer(instanceId, 'MAIN')
            return timer.isAlive()
        return False

    def isStateProp(self, prop, type):
        state = self.curState[type]
        if prop in state:
             return state[prop]
        return True
    
    def runAction(self):
        action = self.curState['stateObj']
        args = {}

        if 'args' in self.curState:
            args = self.curState['args']

        return action(self.block, args)