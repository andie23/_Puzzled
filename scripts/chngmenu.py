from navigator import *
from loader import add_loading_screen
from widgets import Button, Text
from canvas import ChallengeCanvas, ListCanvas
from challenges import CHALLENGE_LIST
from pcache import Scores
from bge import logic
from objproperties import ObjProperties
from utils import frmtTime
from logger import logger
from game import getChallengeId, getDefaultUser

@add_loading_screen
def challengesMain():    
    gdict = logic.globalDict
    challengeList = CHALLENGE_LIST
    scene = logic.getCurrentScene()
    paginator = ListPaginator('challenges', logic)
    positionNodes = ObjProperties().getPropObjGroup(
        'position_node', scene
    )
    positionNodes.reverse()
    perPage = len(positionNodes)
    setCanvas(positionNodes)

    if not paginator.isset():
        paginator.paginate(challengeList, perPage)
    else:
        paginator.load()

    challengeGroup = paginator.get()
    return listChallenges(challengeGroup, positionNodes)


def clearNodes():
    scene = logic.getCurrentScene()
    canvasList = ObjProperties().getPropObjGroup(
        'canvas_id', scene
    )

    for canvas in canvasList:
        if 'main_canvas' not in canvas:
            canvas.endObject()

def setCanvas(positionNodes):
    def nextChallengeList(paginatorID, positionNodes):
        paginator = ListPaginator(paginatorID, logic)
        if paginator.isset():
            paginator.load()
            paginator.next()
            listChallenges(paginator.get(), positionNodes)

    def prevChallengeList(paginatorID, positionNodes):
        paginator = ListPaginator(paginatorID, logic)

        if paginator.isset():
            paginator.load()
            paginator.previous()
            listChallenges(paginator.get(), positionNodes)
        scene = logic.getCurrentScene()
        canvasPositionNode = scene.objects['main_position_node']

    listCanvas = ListCanvas()
    listCanvas.loadStatic()
    
    title = Text(listCanvas.titleTxtObj, 'Challenges')
    nextBtn = Button(listCanvas.nextBtnObj, logic)
    prevBtn = Button(listCanvas.previousBtnObj, logic)

    nextBtn.setOnclickAction(lambda:nextChallengeList('challenges', positionNodes))
    prevBtn.setOnclickAction(lambda:prevChallengeList('challenges', positionNodes))
    listCanvas.show(listCanvas.canvasObj)

def listChallenges(challengeGroup, positionNodes):
    playerID = getDefaultUser('id')
    clearNodes()
    for index, challengeSetup in enumerate(challengeGroup):
        cbody = challengeSetup
        challengeID = getChallengeId(cbody['name'])
        score = Scores(playerID, challengeID)
        score.fetch()
        positionNode = positionNodes[index]
        
        canvasId =  '%s_%s' % (index, cbody['name'].replace(' ','_'))
        canvas = ChallengeCanvas(canvasId)
        canvas.add(positionNode)
        
        title = Text(canvas.titleTxtObj, cbody['name'])
        playBtn = Button(canvas.playBtnObj, logic)
        playBtn.setOnclickAction(navToPuzzle, cbody)

        patBtn = Button(canvas.patternBtnObj, logic)
        patBtn.setOnclickAction(
           overlayPattern, playerID, challengeID ,cbody
        )

        canvas.fadeIn()

        if score.isset():
            Text(canvas.timeTxtObj, frmtTime(score.timeCompleted))
            Text(canvas.movesTxtObj, score.moves)
            Text(canvas.streaksTxtObj, score.streaks)
        else:
            Text(canvas.timeTxtObj, '00:00:00')
            Text(canvas.movesTxtObj, '0')
            Text(canvas.streaksTxtObj, '0')
    return True