from bge import logic
from objproperties import ObjProperties
from list_canvas import ListCanvas
from challenge_canvas import ChallengeCanvas
from challenge_list import CHALLENGE_LIST
from challenge_menu_listerners import OnChallengeListChangeListerner
from list_paginator import ListPaginator

def init():
    from challenge_menu_listerners import OnStartMenuListingListerner
    scene = logic.getCurrentScene()
    setChallengeMenus(scene)

def setChallengeMenus(scene):
    positionNodes = getPositionNodes(scene)
    paginator = getPaginator(CHALLENGE_LIST, positionNodes)
    setMainCanvas(scene, paginator, positionNodes)
    showChallengeList(scene, paginator.get(), positionNodes)

def getPositionNodes(scene):
    return ObjProperties().getPropObjGroup(
        'position_node', scene
    )

def clearPositionNodes(scene):
    canvasList = ObjProperties().getPropObjGroup(
        'canvas_id', scene
    )

    for canvasObj in canvasList:
        if 'main_canvas' in canvasObj:
            continue
        canvasObj.endObject()

def nextChallengeList(paginator, positionNodes):
    paginator.load()
    paginator.next()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

def previousChallengeList(paginator, positionNodes):
    paginator.load()
    paginator.previous()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

def getPaginator(challenges, positionNodes):
    paginator = ListPaginator('challenges', logic)
    positionNodes.reverse()
    itemsPerPage = len(positionNodes)

    if not paginator.isset():
        paginator.paginate(challenges, itemsPerPage)
    else:
        paginator.load()
    return paginator

def setMainCanvas(scene, paginator, positionNodes):
    from challenge_menu_listerners import OnChallengeListChangeListerner
    from button_widget import Button
    from text_widget import Text

    canvas = ListCanvas()
    canvas.load()

    nextButton = Button(canvas.nextBtnObj)
    previousButton = Button(canvas.previousBtnObj)
    
    Text(canvas.pageNumTxtObj, paginator.curIndex + 1)
    nextButton.setOnclickAction(
        lambda: nextChallengeList(paginator, positionNodes)
    )

    previousButton.setOnclickAction(
        lambda: previousChallengeList(paginator, positionNodes)
    )

    OnChallengeListChangeListerner().attach(
        'update_page_number', 
        lambda index, challenges: Text(canvas.pageNumTxtObj, index + 1)
    )

    OnChallengeListChangeListerner().attach(
        'update_challenge_list',
        lambda index, challenges: showChallengeList(scene, challenges, positionNodes)
    )

def showChallengeList(scene, challenges, positionNodes):
    clearPositionNodes(scene)
    for index, challenge in enumerate(challenges):
        # get a position node object by it's index assigned to it
        positionNode = ObjProperties().getObjByPropVal(
            'position_node', index, positionNodes
        )
        canvas = ChallengeCanvas(challenge['id'])
        canvas.add(positionNode, False)
        setChallengeMenu(canvas, challenge)

def setChallengeMenu(canvas, challenge):
    from canvas_effects import dialogPopIn
    from utils import frmtTime
    from pcache import Scores
    from navigator import startPuzzleScene, overlayChallengeViewer
    from player import getPlayerId
    from button_widget import Button
    from text_widget import Text
    
    playerId = getPlayerId()
    challengeId = challenge['id']
    challengeName = challenge['name']
    score = Scores(playerId, challengeId)
    scene = logic.getCurrentScene()

    moves = 0
    time = '00:00:00'
    streaks = 0

    if score.fetch():
        moves = score.moves
        streaks = score.streaks
        time = frmtTime(score.timeCompleted)

    Text(canvas.titleTxtObj, challengeName)
    Text(canvas.timeTxtObj, time)
    Text(canvas.movesTxtObj, moves)
    Text(canvas.streaksTxtObj, streaks)

    Button(canvas.playBtnObj).setOnclickAction(
        lambda: startPuzzleScene(challenge)
    )

    Button(canvas.patternBtnObj).setOnclickAction(
        lambda: overlayChallengeViewer(challenge)
    )

    dialogPopIn(canvas)


