from bge import logic
from objproperties import ObjProperties
from logger import logger
from navigator import SceneHelper
from clock import Clock

log = logger()

def checkTimer(controller):
    instanceId = controller.owner['instance_id']
    timer = Timer(instanceId)

    if timer.isAlive():
        timer.load()
        if timer.curtime() >= timer.timerLimit:
            timer.callback()
            timer.destroy()

class Timer(Clock):
    def __init__(self, instanceId, sceneId=None):
        super(Clock, self).__init__()
        self.shelper = SceneHelper(logic)
        self.id = instanceId
        self.sceneId = sceneId
        self.instanceObj = None
        self.callback = None
        self.timerLimit = None
        self.scene = self.shelper.getscene(self.sceneId)
     
    def load(self):
        instance = logic.globalDict[self.id]
        self.sceneId = instance['scene_id']
        self.callback = instance['callback']
        self.scene = self.shelper.getscene(self.sceneId)
        self.timerLimit = instance['time_limit']
        self.instanceObj = ObjProperties().getObjByPropVal(
            'instance_id', self.id, self.scene.objects
        )
        Clock.__init__(self, self.instanceObj)

    def _addInstance(self):
        obj = ObjProperties()
        idleInstanceList = obj.getPropObjGroup('timer_instance', self.scene, 0)
        idleInstanceObj = idleInstanceList[0]
        idleInstanceObj['instance_id'] = self.id
        self.scene.addObject(idleInstanceObj)
        timerObj = obj.getObjByPropVal('instance_id', self.id, self.scene.objects)
        return timerObj
    
    def _setGlobals(self):
        logic.globalDict[self.id] = {
            'callback' : self.callback,
            'scene_id' : self.sceneId,
            'time_limit' : self.timerLimit
        }

    def isAlive(self):
        return self.id in logic.globalDict

    def destroy(self):
        del logic.globalDict[self.id]
        if self.instanceObj:
            self.instanceObj.endObject()

    def setTimer(self, time, func, *args, **kwargs):
        instanceObj = self._addInstance()
        instanceObj['timer_limit'] = time
        self.timerLimit = time
        self.callback = lambda: func(*args, **kwargs)
        self.instanceObj = instanceObj
        self._setGlobals()
        Clock.__init__(self, instanceObj)