def attach_background_object(func):
    '''
    Decorator adds a background object to a dialog UI object for effect
    and to block the rest of the ui from interaction i.e. buttons.

    As a requirement, dialog method must return Dialog object type
    '''
    def main(*args, **kwargs):
        canvas = func(*args, **kwargs)
        return attachWhiteTransparentBg(canvas.getCanvasObj(), 'HUD')
    return main

def attachWhiteTransparentBg(targetObj, sceneName):
    _attachBg(targetObj, [1.0, 1.0, 1.0, 0.785], sceneName)

def attachInvisibleBg(targetObj, sceneName):
    _attachBg(targetObj, [1.0, 1.0, 1.0, 1.0], sceneName, False)

def _attachBg(targetObj, col, sceneName, visible=True):
    from objproperties import ObjProperties
    from scene_helper import Scene
    
    scene = Scene(sceneName).getscene()
    bg = ObjProperties().getPropObjGroup(
        'background_view', scene, 0
    )[0]
    bg['target_obj'] = str(targetObj)
    bg.visible = visible
    bg.color = col
    scene.addObject(bg)
    bg = ObjProperties().getObjByPropVal('target_obj', 
        str(targetObj), scene.objects
    )
    bg.position = targetObj.position
    # push it back alittle
    bg.position[2] -= 0.4
    bg.setParent(targetObj)
