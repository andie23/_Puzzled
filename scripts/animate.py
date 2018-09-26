from bge import logic
from navigator import SceneHelper
from objproperties import ObjProperties

def check_target_object(func):
    def main(*args, **kwargs):
        shelper = SceneHelper(logic)
        cont = logic.getCurrentController()
        own = ObjProperties(cont.owner)
        instanceID = own.getProp('instance_id')
        
        if instanceID in logic.globalDict:   
            instanceData = logic.globalDict[instanceID]
            scene = shelper.getscene(instanceData['scene_id'])
            scenObjs = scene.objects

            targetObj = own.getObjByPropVal('anim_id', instanceID, scenObjs)
            if not targetObj:
               return cont.owner.endObject()
        return func(*args, **kwargs) 
    return main
           
def initAnimation(sceneID, data):
    targetObj = data['target_obj']
    instanceID = getObjID(targetObj)

    if instanceID not in logic.globalDict:
        data['target_obj'] = setObjAnimID(targetObj, instanceID)
        data['scene_id'] = sceneID
        logic.globalDict[instanceID] = data
        addAnimInstanceObj(instanceID, sceneID, targetObj)   

def getObjID(obj):
    return '_%s' % hash(obj)

def setObjAnimID(obj, animID):
    if 'anim_id' not in obj:
        obj['anim_id'] = animID
    return obj

def addAnimInstanceObj(instanceID, sceneID, targetObj):
    obj = ObjProperties()
    shelper = SceneHelper(logic)
    scene = shelper.getscene(sceneID)
    idleInstance = obj.getPropObjGroup('anim_instance',  scene, 0)
    idleInstance = idleInstance[0]
    idleInstance['instance_id'] = instanceID   
    scene.addObject(idleInstance, targetObj, 0)

@check_target_object
def run():
    controller = logic.getCurrentController()
    own = controller.owner['instance_id']
    animData = logic.globalDict[own]
    playOnce(
        animData['target_obj'],
        animData['anim_name'],
        animData['fstart'],
        animData['fstop'],
        animData['speed'],
    )

@check_target_object
def recordFrames():
    own = logic.getCurrentController().owner
    instanceID = own['instance_id']
    instanceData = logic.globalDict[instanceID]
    targetObj = instanceData['target_obj']

    own['cur_frame'] = targetObj.getActionFrame()

@check_target_object
def onStart():
    controller = logic.getCurrentController()
    own = controller.owner
    instanceID = own['instance_id']
    instanceData = logic.globalDict[instanceID]
    
    if 'on_start_action' not in instanceData:
        return
    
    fstart = instanceData['fstart']
    curFrame = own['cur_frame']
        
    if curFrame >= 1.0:
        own['is_start'] = True
        action = instanceData['on_start_action']
        action()

@check_target_object
def onFinish():
    controller = logic.getCurrentController()
    own = controller.owner
    instanceID = own['instance_id']
    instanceData = logic.globalDict[instanceID]
    
    fstop = instanceData['fstop']
    curFrame = own['cur_frame']
                
    if curFrame >= fstop:
        if 'on_finish_action' in instanceData:
            own['is_stop'] = True
            action = instanceData['on_finish_action']
            action()
        own.endObject()
        del logic.globalDict[instanceID]
        
@check_target_object
def playOnce(obj, name, fstart=0.0, fend=20.0, speed=1.0):
    obj.playAction(
        name, start_frame=fstart, 
        end_frame=fend, speed=speed
    )
