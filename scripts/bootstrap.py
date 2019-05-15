from bge import logic
from navigator import *
from objproperties import ObjProperties
from logger import logger

DEFAULT_SCENE = 'CHALLENGES_MENU'
SCENE_PRELOAD_LIST = [
    'LOADER', 'MAIN', 'HUD', 'DIALOG', 'PATTERN_VIEW',
    'CHALLENGES_MENU', 'ASSESSMENT'
]
log = logger()

def preload():
    if not isPreloadIndexSet():
        addPreloadIndex()
        index = 0
    else:
        index = getPreloadIndex()
        sceneCount = len(SCENE_PRELOAD_LIST) - 1
        if index < sceneCount:
            index = incrementIndex()
        else:
            closePreloadDummy()
            removePreloadIndex()
            logic.getCurrentScene().replace(DEFAULT_SCENE)
            return

    nextScene = SCENE_PRELOAD_LIST[index]
    logic.getCurrentScene().replace(nextScene)
    log.debug("Preloading scene %s", nextScene)

def incrementIndex():
    logic.globalDict['preload_bootstrap_index'] += 1
    return logic.globalDict['preload_bootstrap_index']

def removePreloadIndex():
    del logic.globalDict['preload_bootstrap_index']

def startDefaultScene():
    navToChallenges()

def isPreloadIndexSet():
    return 'preload_bootstrap_index' in logic.globalDict
    
def addPreloadIndex():
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
    
    if isPreloadIndexSet():
        # load scene once to cache and return to PRELOAD scene to cache a new scene
        return scene.replace('PRELOAD')
    
    # Get main Empty object that manages/ initiates/ coordinate activities in 
    # the scene
    main = ObjProperties().getPropObjGroup('_MAIN_', scene, 0)
    log.debug('Main program %s', main)
    if str(main) not in scene.objects:
        scene.addObject(str(main[0]))
