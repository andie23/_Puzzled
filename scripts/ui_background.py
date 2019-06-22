def appendBackground(targetObj, sceneName='HUD'):
    _attachBg(targetObj, [1.0, 1.0, 1.0, 0.785], sceneName)

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
