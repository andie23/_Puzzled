from bge import logic
from objproperties import ObjProperties

def init():
    from challenge_menu_listerners import OnStartMenuListingListerner
    scene = logic.getCurrentScene()
    OnStartMenuListingListerner().attach(
        'clear_position_nodes', lambda: clearPositionNodes(scene)
    )
    setChallengeMenus(scene)

def setChallengeMenus(scene):
    from challenge_list import CHALLENGE_LIST

    positionNodes = getPositionNodes(scene)
    paginator = getPaginator(CHALLENGE_LIST, positionNodes)
    setMainCanvas(paginator, positionNodes)
    showChallengeList(paginator.get(), positionNodes) 

def getPositionNodes(scene):
    return ObjProperties().getPropObjGroup(
        'position_node', scene
    )

def clearPositionNodes(scene):
    canvasList = ObjProperties().getPropObjGroup(
        'canvas_id', scene
    )
    for canvas in canvasList:
        if 'main_canvas' not in canvas:
            canvas.endObject()

def nextChallengeList(paginator, positionNodes):
    from challenge_menu_listerners import OnChallengeListChangeListerner

    paginator.load()
    paginator.next()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

def previousChallengeList(paginator, positionNodes):
    from challenge_menu_listerners import OnChallengeListChangeListerner

    paginator.load()
    paginator.previous()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

def getPaginator(challenges, positionNodes):
    from navigator import ListPaginator

    paginator = ListPaginator('challenges', logic)
    positionNodes.reverse()
    itemsPerPage = len(positionNodes)

    if not paginator.isset():
        paginator.paginate(challenges, itemsPerPage)
    else:
        paginator.load()
    return paginator

def setMainCanvas(paginator, positionNodes):
    from canvas import ListCanvas
    from navigator import ListPaginator
    from challenge_menu_listerners import OnChallengeListChangeListerner
    from button_widget import Button
    from text_widget import Text

    canvas = ListCanvas()
    canvas.loadStatic()
    paginator = ListPaginator('challenges', logic)
    nextButton = Button(canvas.nextBtnObj)
    previousButton = Button(canvas.previousBtnObj)
    
    OnChallengeListChangeListerner().attach(
        'update_page_number', 
        lambda index, challenges: Text(canvas.pageNumTxtObj, index + 1)
    )

    OnChallengeListChangeListerner().attach(
        'update_challenge_list',
        lambda index, challenges: showChallengeList(challenges, positionNodes)
    )

    nextButton.setOnclickAction(
        lambda: nextChallengeList(paginator, positionNodes)
    )

    previousButton.setOnclickAction(
        lambda: previousChallengeList(paginator, positionNodes)
    )
   

def showChallengeList(challenges, positionNodes):
    from canvas import ChallengeCanvas
    from uuid import uuid1

    for index, challenge in enumerate(challenges):
        canvasId = str(uuid1())
        canvas = ChallengeCanvas(canvasId)
        canvas.add(positionNodes[index])
        setChallengeMenu(canvas, challenge)
        canvas.fadeIn()

def setChallengeMenu(canvas, challenge):
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


