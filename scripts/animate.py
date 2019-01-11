from bge import logic
from navigator import SceneHelper
from objproperties import ObjProperties
from logger import logger

log = logger()

def _check_target_object(func):
    '''
    Decorator for checking whether the target object being
    animated is still in the scene. If its not, the animation instance 
    is deleted.

    '''

    def main(*args, **kwargs):
        own = logic.getCurrentController().owner
        animId = own['anim_instance_id']
        animData = getAnimData(animId)

        if animData:   
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

def _getAnimDict():
    if not 'animations' in logic.globalDict:
        logic.globalDict['animations'] = {}
        log.debug('Created animations dictionary')

    return logic.globalDict['animations']
  
def getAnimData(animId):
    if isAnimGlobalSet(animId):
        return _getAnimDict()[animId]
    log.debug("Anim %s not found", animId)
    return {}

def _setAnimData(animId, data):
    _getAnimDict()[animId] = data

def initAnimation(animData, animId=None, persistentInstance=False):
    '''
    Animation entry point. This must be called in other modules to
    start animation process on any object.
    '''

    if not animId:
        animId = getAnimId(animData)

    animData['target_obj']['anim_id'] = animId 
    _setAnimData(animId, animData)
    _addAnimInstanceObj(animId, animData['scene_id'])

def isAnimSet(animId, sceneId):
    return isAnimInstanceObjSet(animId, sceneId) and isAnimGlobalSet(animId)

def isAnimInstanceObjSet(animId, sceneId):
    return _getAnimInstanceObj(animId, sceneId) is not None

def killAnimInstance(animId):
    animData = getAnimData(animId)
    if not animData:
        return

    animInstance = _getAnimInstanceObj(animId, animData['scene_id'])
    
    try:
        if animData['target_obj'].isPlayingAction(1):
            animData['target_obj'].stopAction(1)
    except Exception as error:
        return

    if animInstance:
        animInstance.endObject()

    del animData

def _getAnimInstanceObj(animId, sceneId):
    scene = SceneHelper(logic).getscene(sceneId)
    return ObjProperties().getObjByPropVal(
        'anim_instance_id', animId, scene.objects
    )

def isAnimGlobalSet(animId):
    return animId in _getAnimDict()

def getAnimId(dat):
    return 'anim_%s_%s' % (
        dat['anim_name'], hash(dat['target_obj'])
    )

def _addAnimInstanceObj(animId, sceneId):
    '''
    Adds an object in the scene that will  animate and manage 
    animation for set target object.
    '''
    
    scene = SceneHelper(logic).getscene(sceneId)
    if not isAnimInstanceObjSet(animId, sceneId):
        idleInstance = ObjProperties().getPropObjGroup(
            'anim_instance_id',  scene, 0
        )[0]
        idleInstance['anim_instance_id'] = animId   
        scene.addObject(idleInstance)

@_check_target_object
def _run():
    '''
    Plays the animation only once.
    '''

    animId = logic.getCurrentController().owner['anim_instance_id']
    animData = getAnimData(animId)
    _playOnce(
        animData['target_obj'],
        animData['anim_name'],
        animData['fstart'],
        animData['fstop'],
        animData['speed'],
    )

@_check_target_object
def _recordFrames():
    '''
    Record current animation frames
    '''

    own = logic.getCurrentController().owner
    animId = own['anim_instance_id']
    targetObj = getAnimData(animId)['target_obj']
    own['cur_frame'] = targetObj.getActionFrame()

@_check_target_object
def _onStart():
    '''
    Executes any method set in on_start_action when the animation
    starts on frame 1.
    '''

    own = logic.getCurrentController().owner
    animId = own['anim_instance_id']
    animData = getAnimData(animId)
    
    if own['cur_frame'] >= 1.0:
        own['is_start'] = True
        if 'on_start_action' in animData:
            animData['on_start_action']()

@_check_target_object
def _onFinish():
    '''
    Excutes callback after an animation finishes playing.
    Animation instance is terminated here
    '''
 
    own = logic.getCurrentController().owner
    animId = own['anim_instance_id']
    animData = getAnimData(animId)

    if own['cur_frame'] >= animData['fstop']:
        own['is_stop'] = True
        if 'on_finish_action' in animData:
            animData['on_finish_action']()
        killAnimInstance(animId)

@_check_target_object
def _playOnce(obj, name, fstart=0.0, fend=20.0, speed=1.0):
    obj.playAction(
        name, start_frame=fstart, 
        end_frame=fend, speed=speed
    )
