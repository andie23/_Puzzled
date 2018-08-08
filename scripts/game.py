from bge import logic

def getScene(name):
    sceneList = logic.getSceneList()
    
    for scene in sceneList:
        if name == str(scene):
            return scene
    return None

def killScenes(scope):
    sceneList = logic.getSceneList()
    for scene in sceneList:
        if str(scene) in scope:
            scene.end()

def restartScenes(scope):
    sceneList = logic.getSceneList()
    for scene in sceneList:
        if str(scene) in scope:
            scene.restart()

def restartPuzzle():
    killScenes(['ASSESSMENT'])
    restartScenes(['MAIN', 'HUD'])

def listChallenges():
    scene = logic.getCurrentScene()
    scene.replace('CHALLENGES_MENU')
    killScenes(['ASSESSMENT', 'HUD'])
    