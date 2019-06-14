from bge import logic
from scene_helper import Scene

def startPuzzleScene(challenge = None, isShowInstructions = True):
    from challenge_global_data import LoadedChallengeGlobalData
    from dialog import infoDialog

    loadedChallenge = LoadedChallengeGlobalData(challenge)
    
    if isShowInstructions and loadedChallenge.getInstructions():
        return infoDialog(
            title=loadedChallenge.getName(),
            subtitle=loadedChallenge.getInstructions(),
            callback=lambda:navigate('MAIN')
        )
    navigate('MAIN')

def startChallengeListScene():
    navigate('CHALLENGES_MENU')

def overlayAssessment():
    overlay('ASSESSMENT')

def overlayChallengeViewer(challenge = None):
    from challenge_global_data import LoadedChallengeGlobalData    
    loadedChallenge = LoadedChallengeGlobalData(challenge)
    overlay('PATTERN_VIEW')

def overlayHud():
    overlay('HUD')

def overlayPreloadDummy():
    overlay('PRELOAD_DUMMY')

def closePreloadDummy():
    closeOverlay('PRELOAD_DUMMY')

def closeHudScreen():
    closeOverlay('HUD')

def closePatternScreen():
    closeOverlay('PATTERN_VIEW')
    
def closeAssessmentScreen():
    closeOverlay('ASSESSMENT')

def suspendScene(name):
    scene = Scene(name)
    if scene.isset():
        scene.suspend()

def resumeScene(name):
    scene = Scene(name)
    if scene.isset():
        scene.resume()

def navigate(name):
    Scene(name).addBackground()

def overlay(name):
    Scene(name).addOverlay()

def closeOverlay(name):
    scene = Scene(name)
    if scene.isset():
        scene.remove()


