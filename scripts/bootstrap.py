from bge import logic
from navigator import *
from objproperties import ObjProperties
from logger import logger

SCENE_PRELOAD_LIST = [
    'LOADER', 'MAIN', 'HUD', 'DIALOG', 'PATTERN_VIEW',
    'CHALLENGES_MENU', 'ASSESSMENT'
]
log = logger()

def preload():
    scene = logic.getCurrentScene()
    sceneCount = len(SCENE_PRELOAD_LIST) - 1
    
    if not isPreloaderSet():
        startPreloadBootstrap()
        index = 0
    else:
        index = getPreloadIndex()
        if index >= sceneCount:
            deletePreloadBootstrap()
            setDefaultScene()
            return
        else:
            index = incrementIndex()
    nextScene = SCENE_PRELOAD_LIST[index]
    log.debug("Preloading scene %s", nextScene)
    scene.replace(nextScene)

def incrementIndex():
    logic.globalDict['preload_bootstrap_index'] += 1
    return logic.globalDict['preload_bootstrap_index']

def deletePreloadBootstrap():
    del logic.globalDict['preload_bootstrap_index']

def setDefaultScene():
    navToChallenges()

def isPreloaderSet():
    return 'preload_bootstrap_index' in logic.globalDict
    
def startPreloadBootstrap():
    if not isPreloaderSet():
        logic.globalDict['preload_bootstrap_index'] = 0

def getPreloadIndex():
    return logic.globalDict['preload_bootstrap_index']

def loadMain(sceneId=None):
    '''
    Strictly used by scene bootstrappers
    '''
    if sceneId:
        scene= SceneHelper(logic).getscene(sceneId)
    
    if not scene:
        scene = logic.getCurrentScene()
    
    if isPreloaderSet():
        # current scene is cached, return to PRELOAD scene
        # during bootstrap..
        scene.replace('PRELOAD')
    else:
        # get main program in the scene
        _main_ = ObjProperties().getPropObjGroup('_MAIN_', scene, 0)
        log.debug('Main program %s', _main_)
        if str(_main_) not in scene.objects:
            scene.addObject(str(_main_[0]))
