from bge import logic

def navToChallenges():
    navigate('CHALLENGES_MENU')
    
def navToPuzzle(data):
    logic.globalDict['gsetup'] = data
    navigate('MAIN')

def overlayAssessment(data):
    logic.globalDict['play_session'] = data
    overlay('ASSESSMENT', 1)

def overlayPattern(data):
    logic.globalDict['setup_to_visualise'] = data
    overlay('PATTERN_VIEW', 1)

def overlayHud():
    overlay('HUD')

def closeHudScreen():
    closeOverlay('HUD')

def closePatternScreen():
    closeOverlay('PATTERN_VIEW')
    
def closeAssessmentScreen():
    closeOverlay('ASSESSMENT')

def navigate(name):
    shelper = SceneHelper(logic)
    if not shelper.isset(name):
        shelper.switchscene(name)

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
            if name == str(scene):
                return scene
        return None

    def addoverlay(self, name, disableBgScene=0):
        gdict = logic.globalDict['Navigator']['overlay']
        if disableBgScene == 1:
            gdict[name] = {'prev_scene' : self.curscene}
            self.curscene.suspend()
        self.logic.addScene(name, 1)

    def removeOverlay(self, name):
        gdict = logic.globalDict['Navigator']['overlay']
        if name in gdict:
            suspscene = gdict[name]['prev_scene']
            suspscene.resume()
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

class ListPaginator:
    def __init__(self, name, logic):
        self.gdict = logic.globalDict
        self.pgID = '%s.paginator' % name
        self.perPage = 0
        self.groupList = []
        self.curIndex = 0
    
    def isset(self):
        return self.pgID in self.gdict
    
    def load(self):
        props = self.gdict[self.pgID]
        self.perPage = props['perPage']
        self.groupList = props['groupList']
        self.curIndex = props['curIndex']

    def updateGlobalIndex(self, val):
        self.gdict[self.pgID]['curIndex'] = val 

    def paginate(self, listItems, itemsPerpage):
        groupList = self.groupItems(listItems, itemsPerpage)
        self.perPage = itemsPerpage
        self.groupList = groupList
        
        self.gdict[self.pgID] = {
            'perPage': itemsPerpage,
            'groupList' : groupList,
            'curIndex' : self.curIndex
        }

    def get(self):
        return self.groupList[self.curIndex]
    
    def next(self):
        groupLen = len(self.groupList) -1
        if self.curIndex >= groupLen:
            self.curIndex = 0
        else:
            self.curIndex += 1
        self.updateGlobalIndex(self.curIndex)
        return self.groupList[self.curIndex]

    def previous(self):
        if self.curIndex <= 0:
            groupLen = len(self.groupList) -1
            self.curIndex = groupLen
        else:
            self.curIndex -= 1
        self.updateGlobalIndex(self.curIndex)
        return self.groupList[self.curIndex]

    def groupItems(self, listItems, itemsPerGroup):
        curIndex = 0
        itemGroupList = [[]]

        for item in listItems:
            if len(itemGroupList[curIndex]) >= itemsPerGroup:
                curIndex +=1
                itemGroupList.append([])
            itemGroupList[curIndex].append(item)
        return itemGroupList