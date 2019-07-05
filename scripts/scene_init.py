from bge import logic
from objproperties import ObjProperties

def init():
    scene = logic.getCurrentScene()
    # Detect if program is in scene preload mode
    # and jump back to PRELOAD scene
    if '_preload_scene' in logic.globalDict:
        scene.replace('PRELOAD')
        return

    sceneInitObj = ObjProperties().getPropObjGroup(
        '_SCENE_CONTROLLER_', scene, 0
    )

    if not sceneInitObj:
        return

    if sceneInitObj not in scene.objects:
        scene.addObject(str(sceneInitObj[0]))
