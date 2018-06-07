###################################
# Author: Andrew Mfune
# Date: 07/06/2018
###################################
from copy import deepcopy
from bge import logic
from logger import logger
from threading import Timer
globalDict = logic.globalDict

log = logger()

class State():
    def __init__(self, block, state):
        self.name = state['stateObj'].__name__
        self.block = block
        self.id = 'b%s' % block.getBlockNumber()
        
        if self.id not in globalDict:
            log.debug('Initialising %s in globalDict', self.id)
            globalDict[self.id] = {'states' : {}}

        if self.name not in self.states:
            log.debug('Appending state %s to %s in globalDict', state, self.id)
            self.setStateInGlobalDict(state)

    @property
    def states(self):
        return globalDict[self.id]['states']

    @property
    def curState(self):
        return self.states[self.name]

    @property
    def isBlockInScope(self):

        if 'scope' not in self.curState:
            return -1

        scope = self.curState['scope']

        if self.block.getBlockNumber() in scope:
            return 1

        return 0

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
    def isDelayTimerActive(self):
        if 'timerObj' in self.curState['delay']:
            delay = self.curState['delay']
            return delay['timerObj'].is_alive()
        return False

    @property
    def isDurationTimerActive(self):
        if 'timerObj' in self.curState['duration']:
            duration = self.curState['duration']
            return duration['timerObj'].is_alive()
        return False

    @property
    def expiryActions(self):
        return self.curState['duration']['expiryActions']

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
            timerObj = delay['timerObj']
            timerObj.cancel()
            self.setIsDelayInit(False)
            log.debug('%s state %s delay has been cancelled', self.id, self.name)

    def cancelDuration(self):
        if self.isDurationTimerActive:
            duration = self.curState['duration']
            timerObj = duration['timerObj']
            timerObj.cancel()
            self.setIsDurationInit(False)
            log.debug('%s state %s duration has been cancelled', self.id, self.name)

    def startDelay(self):
        delay = self.curState['delay']
        time = delay['time']

        if not 'timerObj' in delay:
            log.debug('%s Starting delay for %s', self.id, self.name)
            self.curState['timerObj'] = None
            self.setIsDelayInit(False)
            self.setIsDelayExp(False)
    
        if not self.isDelayInit:
            delay['timerObj'] = Timer(
                time, self.setIsDelayExp, [True]
            )
            delay['timerObj'].start()
            self.setIsDelayInit(True)
            log.debug('%s state %s is starting a delay', self.id, self.name)
            
    def startDuration(self):
        duration = self.curState['duration']
        time = duration['time']

        if not 'timerObj' in duration:
            log.debug('Starting Duration for %s', self.name)    
            self.setIsDurationInit(False)
            self.setIsDurationExp(False)
            
        if not self.isDurationInit:
            duration['timerObj'] = Timer(
                time, self.setIsDurationExp, [True]
            )
            duration['timerObj'].start()
            self.setIsDurationInit(True)
            log.debug('%s state %s is starting a duration', self.id, self.name)

    
    def runAction(self):
        action = self.curState['stateObj']
        args = {}

        if 'args' in self.curState:
            args = self.curState['args']

        return action(self.block, args)