from bge import logic
from threading import Timer
from logger import logger

log = logger()
globalDict = logic.globalDict

class StateProps():
    def __init__(self, blockNum, stateName):
        self.blockNum = blockNum
        self.stateName = stateName
        self._stateHeader = self.getStateHeader()
        self._tThreadHeader = self.getTthreadHeader()
        
        if not self.isStateSet():
            self.setStateDefaults()

        if not self.isTthreadSet():
            self.setTthreadDefaults()

    def isDelayInit(self):
        return self.getStateByName('isDelayInit')
    
    def isDurationExpired(self):
        return self.getStateByName('isDurationExpired')
    
    def isDurationInit(self):
        return self.getStateByName('isDurationInit')

    def isDelayExpired(self):
        return self.getStateByName('isDelayExpired')
   
    def setStateProp(self, prop, val):
        globalDict[self._stateHeader][prop] = val
    
    def setIsDelayInit(self, val):
        self.setStateProp('isDelayInit', val)
    
    def setIsDurationExpired(self, val):
        self.setStateProp('isDurationExpired', val)
    
    def setIsDurationInit(self, val):
        self.setStateProp('isDurationInit', val)

    def setIsDelayExpired(self, val):
        self.setStateProp('isDelayExpired', val)

    def setTthreadProp(self, prop, val):
        globalDict[self._tThreadHeader][prop] = val

    def setStateDefaults(self):
         globalDict[self._stateHeader] = self.getStateDefaults()

    def setTthreadDefaults(self):
        globalDict[self._tThreadHeader] = {}
    
    def isStateSet(self):
        return self._stateHeader in globalDict
   
    def isTthreadSet(self):
        return self._tThreadHeader in globalDict
    
    def getStateDefaults(self):
        return {
            'isDurationExpired': False,
            'isDelayExpired' : False,
            'isDurationInit' : False,
            'isDelayInit' : False
        }
    
    def getStateList(self):
        return globalDict[self._stateHeader]        
    
    def getStateByName(self, prop):
        return globalDict[self._stateHeader][prop]
    
    def getTthreads(self):
        return globalDict[self._tThreadHeader]
        
    def getTthreadByName(self, prop):
        return globalDict[self._tThreadHeader].get(prop)
    
    def cancelTthread(self, threadName):
        timerThreads = self.getTthreads()
       
        if threadName in timerThreads:
            timer = self.getTthreadByName(threadName)
            timer.cancel()
            if not timer.is_alive():
                del timerThreads[threadName]
                log.debug('Thread %s has been cancelled', threadName) 

    def cancelTthreads(self, excludedStates=[]):
        timerThreads = self.getTthreads()
        
        for timerThread in timerThreads:
            if timerThread not in excludedStates:
                self.cancelTimerThread(timerThread)

    def getStateHeader(self):
        return '%s_%s.state' % (self.blockNum, self.stateName)

    def getTthreadHeader(self):        
        return '%s_%s.tthread' % (self.blockNum, self.stateName)
    
class StateHandler(StateProps):
    def __init__(self, state, block, controller):
        self.stateObj = state['state']['obj']
        self.args = state['state']['args']
        self.duration = state['duration']
        self.delay = state['delay']
        self.controller = controller
        self.block = block
        self.blockNum = block.getBlockNumber()
        self.stateName = self.stateObj.__name__
        self._stateHeader = self.getStateHeader()
        self._tThreadHeader = self.getTthreadHeader()

        super().__init__(self.blockNum, self.stateName)

    def startDelay(self):
        if not self.isDelayInit():
            self.initStateDelay()
   
    def startDuration(self):
        if not self.isDurationInit(): 
            self.initStateDuration()

    def run(self):
        return self.stateObj(self.block, self.controller, self.args)

    def initStateDelay(self):
        self.startTimerThread(
            self.delay, self.setIsDelayExpired, True
        )
        self.setIsDelayInit(True)

    def initStateDuration(self):
        self.startTimerThread(
            self.duration, self.setIsDurationExpired, True
        )
        self.setIsDurationInit(True)
    
    def isDelaySet(self):
        return self.delay >= 1
    
    def isDurationSet(self):
        return self.duration >= 1

    def startTimerThread(self, duration, obj, *args, **kwargs):
        timerThreads = self.getTthreads()
        
        if self._stateHeader not in timerThreads:
            timer = Timer(duration, obj, args, kwargs)
            self.setTthreadProp(
                self._stateHeader, timer
        )
        timer = self.getTthreadByName(self._stateHeader)
        timer.start()
        log.debug(
            'Thread %s started.. Thread list: %s',
             self._stateHeader, globalDict[self._tThreadHeader]
        )
    