from bge import logic
from navigator import SceneHelper
from objproperties import ObjProperties


def check_target_object(func):
    '''
    Decorator for checking whether the target object being
    animated is still in the scene. If its not, the animation instance 
    is deleted.

    '''

    def main(*args, **kwargs):
        own = logic.getCurrentController().owner
        animId = own['instance_id']

        if animId in logic.globalDict:   
            animData = logic.globalDict['animations'][animId]
            scene = SceneHelper(logic).getscene(
                animData['scene_id']
            )
            targetObj = ObjProperties().getObjByPropVal(
                'anim_id', animId, scene.objects
            )
            if not targetObj:
               return killAnimInstance(animId)
        return func(*args, **kwargs) 
    return main
      
def initAnimation(animData, animId=None, persistentInstance=False):
    '''
    Animation entry point. This must be called in other modules to
    start animation process on any object.
    '''
    if not 'animations' in logic.globalDict:
        logic.globalDict['animations'] = {}

    if not animId:
        animId = getAnimId(animData)
    
    animData['target_obj']['anim_id'] = animId
    logic.globalDict['animations'][animId] = animData
    addAnimInstanceObj(animId, animData['scene_id'])

def isAnimSet(animId, sceneId):
    return isAnimInstanceObjSet(animId, sceneId) and isAnimGlobalSet(animId)

def isAnimInstanceObjSet(animId, sceneId):
    return getAnimInstanceObj(animId, sceneId) is not None

def killAnimInstance(animId):
    animData = logic.globalDict['animations'][animId] 
    animInstance = getAnimInstanceObj(animId, animData['scene_id'])

    if animData['target_obj'].isPlayingAction(1):
        animData['target_obj'].stopAction(1)

    if animInstance:
        animInstance.endObject()

    del animData

def getAnimInstanceObj(animId, sceneId):
    scene = SceneHelper(logic).getscene(sceneId)
    return ObjProperties().getObjByPropVal(
        'instance_id', animId, scene.objects
    )

def isAnimGlobalSet(animId):
    return animId in logic.globalDict['animations']

def getAnimId(dat):
    return 'anim_%s_%s' % (
        dat['anim_name'], hash(dat['target_obj'])
    )

def addAnimInstanceObj(animId, sceneId):
    '''
    Adds an object in the scene that will  animate and manage 
    animation for set target object.
    '''
    
    scene = SceneHelper(logic).getscene(sceneId)
    if not isAnimInstanceObjSet(animId, sceneId):
        idleInstance = ObjProperties().getPropObjGroup(
            'anim_instance',  scene, 0
        )[0]
        idleInstance['instance_id'] = animId   
        scene.addObject(idleInstance)

@check_target_object
def run():
    '''
    Plays the animation only once.
    '''

    animId = logic.getCurrentController().owner['instance_id']
    animData = logic.globalDict['animations'][animId]
    playOnce(
        animData['target_obj'],
        animData['anim_name'],
        animData['fstart'],
        animData['fstop'],
        animData['speed'],
    )

@check_target_object
def recordFrames():
    '''
    Record current animation frames
    '''

    own = logic.getCurrentController().owner
    animId = own['instance_id']
    targetObj = logic.globalDict['animations'][animId]['target_obj']
    own['cur_frame'] = targetObj.getActionFrame()

@check_target_object
def onStart():
    '''
    Executes any method set in on_start_action when the animation
    starts on frame 1.
    '''

    own = logic.getCurrentController().owner
    animId = own['instance_id']
    animData = logic.globalDict['animations'][animId]
    
    if 'on_start_action' in animData:
        if own['cur_frame'] >= 1.0:
            own['is_start'] = True
            animData['on_start_action']()

@check_target_object
def onFinish():
    '''
    Excutes callback after an animation finishes playing.
    Animation instance is terminated here
    '''
 
    own = logic.getCurrentController().owner
    animId = own['instance_id']
    animData = logic.globalDict['animations'][animId]

    if own['cur_frame'] >= animData['fstop']:
        if 'on_finish_action' in animData:
            own['is_stop'] = True
            animData['on_finish_action']()

        killAnimInstance(animId)

@check_target_object
def playOnce(obj, name, fstart=0.0, fend=20.0, speed=1.0):
    obj.playAction(
        name, start_frame=fstart, 
        end_frame=fend, speed=speed
    )
