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
        self.id = str(block.blockID)
        
        if self.id not in globalDict:
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
        duration = self.curState['duration']
        if 'resetInit' in duration:
             return duration['resetInit']
        return True
    
    @property
    def isDelayInitReset(self):
        delay = self.curState['delay']
        if 'resetInit' in delay:
             return delay['resetInit']
        return True
        
    @property
    def isDurationExpReset(self):
        duration = self.curState['duration']
        if 'resetExp' in duration:
             return duration['resetExp']
        return True
    
    @property
    def isDelayExpReset(self):
        delay = self.curState['delay']
        if 'resetExp' in delay:
             return delay['resetExp']
        return True

    @property
    def isDurationTimerActive(self):
        if 'timerObj' in self.curState['duration']:
            duration = self.curState['duration']
            return duration['timerObj'].is_alive()
        return False

    @property
    def isDelayTimerActive(self):
        if 'timerObj' in self.curState['delay']:
            delay = self.curState['delay']
            return delay['timerObj'].is_alive()
        return False

    @property
    def isDurationTimerReset(self):
        duration = self.curState['duration']
        if 'resetTimer' in duration:
             return duration['resetTimer']
        return True

    @property
    def isDelayTimerReset(self):
        delay = self.curState['delay']
        if 'resetTimer' in delay:
             return delay['resetTimer']
        return True

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

    def cancelDuration(self):
        if self.isDurationTimerActive:
            duration = self.curState['duration']
            timerObj = duration['timerObj']
            timerObj.cancel()
            self.setIsDurationInit(False)

    def startDelay(self):
        delay = self.curState['delay']
        time = delay['time']

        if not 'timerObj' in delay:
            self.curState['timerObj'] = None
            self.setIsDelayInit(False)
            self.setIsDelayExp(False)
    
        if not self.isDelayInit:
            delay['timerObj'] = Timer(
                time, self.setIsDelayExp, [True]
            )
            delay['timerObj'].start()
            self.setIsDelayInit(True)
            
    def startDuration(self):
        duration = self.curState['duration']
        time = duration['time']

        if not 'timerObj' in duration:
            self.setIsDurationInit(False)
            self.setIsDurationExp(False)
            
        if not self.isDurationInit:
            duration['timerObj'] = Timer(
                time, self.setIsDurationExp, [True]
            )
            duration['timerObj'].start()
            self.setIsDurationInit(True)

    
    def runAction(self):
        action = self.curState['stateObj']
        args = {}

        if 'args' in self.curState:
            args = self.curState['args']

        return action(self.block, args)