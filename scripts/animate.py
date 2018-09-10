from bge import logic
from navigator import SceneHelper

def initAnimation(instanceId, sceneID, data):
    if instanceId not in logic.globalDict:
        data['obj_name'] = str(data['obj'])
        logic.globalDict[instanceId] = data
        shelper = SceneHelper(logic)
        scene = shelper.getscene(sceneID)
        idleInstance = scene.objectsInactive['anim_instance']
        idleInstance['instance_id'] = instanceId
        scene.addObject(idleInstance, data['obj'], 0)

def run(controller):
    own = controller.owner['instance_id']
    animData = logic.globalDict[own]
    playOnce(
        animData['obj'],
        animData['anim_name'],
        animData['fstart'],
        animData['fstop'],
        animData['speed'],
    )

def recordFrames(controller):
    shelper = SceneHelper(logic)
    scene = shelper.getscene('CHALLENGES_MENU')
    objs = scene.objects
    own = controller.owner
    instanceID = own['instance_id']
    animData = logic.globalDict[instanceID]
    obj = animData['obj']
    
    if animData['obj_name'] in objs:
        own['cur_frame'] = obj.getActionFrame()


def onStart(controller):
    own = controller.owner
    instanceID = own['instance_id']
    animData = logic.globalDict[instanceID]
    
    if 'on_start_action' not in animData:
        return
    
    fstart = animData['fstart']
    curFrame = own['cur_frame']
        
    if curFrame >= 1.0:
        own['is_start'] = True
        action = animData['on_start_action']
        action()
    
def onFinish(controller):
    own = controller.owner
    instanceID = own['instance_id']
    animData = logic.globalDict[instanceID]
    
    fstop = animData['fstop']
    curFrame = own['cur_frame']
                
    if curFrame >= fstop:
        if 'on_finish_action' in animData:
            own['is_stop'] = True
            action = animData['on_finish_action']
            action()
        own.endObject()
        del logic.globalDict[instanceID]
        

def playOnce(obj, name, fstart=0.0, fend=20.0, speed=1.0):
    obj.playAction(
        name, start_frame=fstart, 
        end_frame=fend, speed=speed
    )
