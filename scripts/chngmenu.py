from navigator import *
from widgets import Button, Text
from canvas import ChallengeCanvas, ListCanvas
from challenges import CHALLENGE_LIST
from pcache import Scores
from bge import logic
from objproperties import ObjProperties
from utils import frmtTime
from logger import logger

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
    listChallenges(challengeGroup, positionNodes)

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

def clearNodes():
    scene = logic.getCurrentScene()
    canvasList = ObjProperties().getPropObjGroup(
        'canvas_id', scene
    )

    for canvas in canvasList:
        if 'main_canvas' not in canvas:
            canvas.endObject()

def setCanvas(positionNodes):
    scene = logic.getCurrentScene()
    canvasPositionNode = scene.objects['main_position_node']

    listCanvas = ListCanvas(logic)
    listCanvas.add('list_canvas', canvasPositionNode)
    
    title = Text(listCanvas.titleTxtObj, 'Challenges')
    nextBtn = Button(listCanvas.nextBtnObj, logic)
    prevBtn = Button(listCanvas.previousBtnObj, logic)

    nextBtn.setOnclickAction(lambda:nextChallengeList('challenges', positionNodes))
    prevBtn.setOnclickAction(lambda:prevChallengeList('challenges', positionNodes))

def listChallenges(challengeGroup, positionNodes):
    playerID = logic.globalDict['player']['id']
    canvas = ChallengeCanvas(logic)
    clearNodes()
    for index, challengeSetup in enumerate(challengeGroup):
        cbody = challengeSetup
        challengeID = '%s_%s' % (
            cbody['pattern'], cbody['eventScript']
        )

        score = Scores(playerID, challengeID)
        positionNode = positionNodes[index]
        
        canvasID =  '%s_%s' % (index, cbody['name'].replace(' ','_'))
        canvas.add(canvasID, positionNode)
        
        title = Text(canvas.titleTxtObj, cbody['name'])
        playBtn = Button(canvas.playBtnObj, logic)
        playBtn.setOnclickAction(navToPuzzle, cbody)

        patBtn = Button(canvas.patternBtnObj, logic)
        patBtn.setOnclickAction(overlayPattern, cbody)

        if score.isset():
            Text(canvas.timeTxtObj, frmtTime(score.timeCompleted))
            Text(canvas.movesTxtObj, score.moves)
            Text(canvas.statusTxtObj, 'Played')
        else:
            Text(canvas.timeTxtObj, '00:00:00')
            Text(canvas.movesTxtObj, '0')
            Text(canvas.statusTxtObj, 'Not Played')
