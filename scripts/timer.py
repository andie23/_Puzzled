from bge import logic
from objproperties import ObjProperties
from logger import logger
from navigator import SceneHelper
from clock import Clock

log = logger()

def checkTimer(controller):
    own = controller.owner
    curTime = own['timer']
    limit = own['timer_limit']

    if curTime >= limit:
        instanceId = own['instance_id']
        if instanceId in logic.globalDict:
            callback = logic.globalDict[instanceId]['callback'] 
            callback()
            own.endObject()
            del logic.globalDict[instanceId]

class Timer(Clock):
    def __init__(self, instanceId, sceneId=None):
        super(Clock, self).__init__()
        self.id = instanceId
        self.sceneId = sceneId
        self.instanceObj = None
        self.callback = None
        shelper = SceneHelper(logic)
        self.scene = shelper.getscene(sceneId)

    def load(self):
        obj = ObjProperties()
        instance = logic.globalDict[self.id]
        self.scene = instance['scene']
        self.sceneId = str(self.scene)
        self.instanceObj = obj.getObjByPropVal('instance_id', self.id, self.scene.objects)

    def _addInstance(self):
        obj = ObjProperties()
        idleInstanceList = obj.getPropObjGroup('timer_instance', self.scene, 0)
        idleInstanceObj = idleInstanceList[0]
        idleInstanceObj['instance_id'] = self.id
        self.scene.addObject(idleInstanceObj)
        timerObj = obj.getObjByPropVal('instance_id', self.id, self.scene.objects)
        return timerObj
    
    def _setGlobals(self):
        log.debug('Setting globals')
        logic.globalDict[self.id] = {
            'callback' : self.callback,
            'scene' : self.scene
        }
    
    def isAlive(self):
        return self.id in logic.globalDict

    
    def destroy(self):
        self.instanceObj.endObject()
        del logic.globalDict[self.id]

    def setTimer(self, time, func, *args, **kwargs):
        instanceObj = self._addInstance()
        instanceObj['timer_limit'] = time
        self.callback = lambda: func(*args, **kwargs)
        Clock.__init__(self, logic, self.sceneId, instanceObj)
        self._setGlobals()
        self.instanceObj = instanceObj