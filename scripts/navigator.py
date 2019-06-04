from bge import logic

def startPuzzleScene(challenge = None, isShowInstructions = True):
    from challenge_global_data import LoadedChallengeGlobalData
    from dialog import infoDialog

    loadedChallenge = LoadedChallengeGlobalData(challenge)
    
    if isShowInstructions and loadedChallenge.getInstructions():
        def onDialogBtnClick():
            if SceneHelper(logic).isset('MAIN'):
                closeDialogScreen()
            else:
                navigate('MAIN')

        overlayDialog()
        return infoDialog(
            title=loadedChallenge.getName(),
            subtitle=loadedChallenge.getInstructions(),
            callback=onDialogBtnClick
        )
    navigate('MAIN')   

def startChallengeListScene():
    navigate('CHALLENGES_MENU')

def overlayLoadingScreen():
    overlay('LOADER', 1)

def overlayDialog():
    overlay('DIALOG', 2)

def overlayAssessment():
    overlay('ASSESSMENT', 2)

def overlayChallengeViewer(challenge = None):
    from challenge_global_data import LoadedChallengeGlobalData    
    loadedChallenge = LoadedChallengeGlobalData(challenge)
    overlay('PATTERN_VIEW', 2)

def overlayHud():
    overlay('HUD')

def closePreloadDummy():
    closeOverlay('PRELOAD_DUMMY')

def closeLoadingScreen():
    closeOverlay('LOADER')

def closeDialogScreen():
    closeOverlay('DIALOG')

def closeHudScreen():
    closeOverlay('HUD')

def closePatternScreen():
    closeOverlay('PATTERN_VIEW')
    
def closeAssessmentScreen():
    closeOverlay('ASSESSMENT')

def closeConfirmationDialogScreen():
    closeOverlay('CONFIRMATION_DIALOG')

def navigate(name):
    shelper = SceneHelper(logic)

    if not shelper.isset(name):
        return shelper.switchscene(name)

def overlay(name, disableBgScene=0):
    shelper = SceneHelper(logic)
    if not shelper.isset(name):
        shelper.addoverlay(name, disableBgScene)

def closeOverlay(name):
    shelper = SceneHelper(logic)
    if shelper.isset(name):
       shelper.removeOverlay(name) 

class SceneHelper:
    def __init__(self, logic):
        self.sceneList = logic.getSceneList()
        self.curscene = logic.getCurrentScene()

        if 'Navigator' not in logic.globalDict:
            logic.globalDict['Navigator'] = {}
            logic.globalDict['Navigator']['overlay'] = {}

        self.logic = logic

    def isset(self, name):
        return True if self.getscene(name) else False
    
    def getscene(self, name):        
        for scene in self.sceneList:
            if str(scene) == name:
                return scene
        return None

    def restart(self, scope):
        for scene in self.sceneList:
            if str(scene) in scope:
                scene.restart()

    def pause(self, scope):
        for scene in self.sceneList:
            if str(scene) in scope:
                scene.suspend()
    
    def resume(self, scope):
        for scene in self.sceneList:
            if str(scene) in scope:
                scene.resume()

    def addoverlay(self, name, disableBgScene=0):
        gdict = logic.globalDict['Navigator']['overlay']
        
        if disableBgScene == 1:
            gdict[name] = {
                'suspend_list' : [self.curscene]
            }
            self.curscene.suspend()

        elif disableBgScene == 2:
            gdict[name] = {'suspend_list' : []}
            for scene in self.sceneList:
                gdict[name]['suspend_list'].append(scene)
                scene.suspend()
        self.logic.addScene(name, 1)

    def removeOverlay(self, name):
        gdict = logic.globalDict['Navigator']['overlay']
        if name in gdict:
            suspendlist = gdict[name]['suspend_list']
            for scene in suspendlist:
                scene.resume()
            gdict.pop(name)
        self.killscene(name)

    def killscene(self, name):
        scene = self.getscene(name)
        scene.end()

    def switchscene(self, name):
        if len(self.sceneList) > 1:
            for scene in self.sceneList:
                if str(scene) == name:
                    continue
                scene.end()
        self.curscene.replace(name)
