from bge import logic
from objproperties import ObjProperties
from logger import logger
from timer import Timer
from scene_helper import Scene
DEFAULT_SCENE = 'CHALLENGES_MENU'
SCENE_PRELOAD_LIST = [
    'MAIN', 'HUD', 'CHALLENGES_MENU'
]

def init():
    def preloadScenes():
        if preload(Scene('PRELOAD').getscene()):
            Scene('HUD').addOverlay()
            Scene(DEFAULT_SCENE).addBackground()

    if 'preload_scene_init' not in logic.globalDict:
        '''
        Add an overlay and set a timer to start preloading
        scenes
        '''
        logic.globalDict['preload_scene_init'] = True
        Scene('PRELOAD_DUMMY').addOverlay()
        timer = Timer('Scene_Preloader', 'PRELOAD')
        timer.setTimer(6.0, preloadScenes)
        timer.start()
        return
    preloadScenes()

def preload(scene):
    sceneCount = len(SCENE_PRELOAD_LIST) - 1
    curScenePreloadIndex = 0
    globDict = logic.globalDict
    
    if 'cur_scene_preload_index' not in globDict:
        globDict['cur_scene_preload_index'] = 0
        globDict['_preload_scene'] = True
    
    curScenePreloadIndex = globDict['cur_scene_preload_index']

    if curScenePreloadIndex < sceneCount:
        nextScene = SCENE_PRELOAD_LIST[curScenePreloadIndex]
        globDict['cur_scene_preload_index'] += 1
        scene.replace(nextScene)
        return False

    del globDict['cur_scene_preload_index']
    del globDict['_preload_scene']
    return True
