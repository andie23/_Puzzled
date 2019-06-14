from bge import logic
from objproperties import ObjProperties
from logger import logger
from scene_helper import Scene
from clock import Clock

log = logger()

def checkTimer(controller): 
    instanceId = controller.owner['instance_id']
    timer = Timer(instanceId)

    if not timer.isAlive():
        return

    timer.load()
    
    if not timer.isActive:
        return

    if not timer.timerLimit:
        timer.destroy()

    if timer.curtime() >= timer.timerLimit:
        try:
            timer.callback()
            timer.destroy()
        except Exception as error:
            log.debug('Timer Exception: %s', error)
            timer.destroy()

class Timer(Clock):
    def __init__(self, instanceId, sceneId=None):
        super(Clock, self).__init__()
        self.id = instanceId
        self.sceneId = sceneId
        self.instanceObj = None
        self.callback = None
        self.timerLimit = None
        self.scene = Scene(sceneId).getscene()

        if 'timer_instances' not in logic.globalDict:
            logic.globalDict['timer_instances'] = {}
    
    def load(self):
        instance = logic.globalDict['timer_instances'][self.id]
        self.sceneId = instance['scene_id']
        self.callback = instance['callback']
        self.scene = Scene(self.sceneId).getscene()
        self.timerLimit = instance['time_limit']
        self.instanceObj = ObjProperties().getObjByPropVal(
            'instance_id', self.id, self.scene.objects
        )
        Clock.__init__(self, self.instanceObj)

    def _addInstance(self):
        log.debug("Creating timer instance %s", self.id)
        obj = ObjProperties()
        idleInstanceList = obj.getPropObjGroup('timer_instance', self.scene, 0)
        idleInstanceObj = idleInstanceList[0]
        idleInstanceObj['instance_id'] = self.id
        self.scene.addObject(idleInstanceObj)
        timerObj = obj.getObjByPropVal('instance_id', self.id, self.scene.objects)
        return timerObj
    
    def _setGlobals(self):
        logic.globalDict['timer_instances'][self.id] = {
            'callback' : self.callback,
            'scene_id' : self.sceneId,
            'time_limit' : self.timerLimit
        }

    def isAlive(self):
        return self.id in logic.globalDict['timer_instances']

    def destroy(self):
        log.debug("destroying timer instance %s", self.id)
        if not self.instanceObj:
            return
        self.instanceObj.endObject()
        del logic.globalDict['timer_instances'][self.id]

    def setTimer(self, time, func, *args, **kwargs):
        instanceObj = self._addInstance()
        self.timerLimit = time
        self.callback = lambda: func(*args, **kwargs)
        self.instanceObj = instanceObj
        self._setGlobals()
        Clock.__init__(self, instanceObj)