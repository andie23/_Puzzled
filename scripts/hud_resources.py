from bge import logic

def loadInGameHud():
    _addObjResource('ingame_menu')

def loadPuzzlePatternViewer(challenge=None):
    if challenge:
        from challenge_global_data import LoadedChallengeGlobalData
        loadedChallenge = LoadedChallengeGlobalData(challenge)
    _addObjResource('challenge_viewer')

def loadAssessmentView():
    _addObjResource('assessment_view')

def removeInGameHud():
    _removeObjResource('ingame_menu')

def getHudScene():
    from scene_helper import Scene
    return Scene('HUD')

def _removeObjResource(name):
    scene = getHudScene().getscene()

    if name in scene.objects:
        scene.objects[name].endObject()

def _addObjResource(name):
    from objproperties import ObjProperties
    
    scene = getHudScene().getscene()
    obj = ObjProperties().getPropObjGroup(name, scene, 0)

    if str(obj) not in scene.objects:
        scene.addObject(str(obj[0]))

    