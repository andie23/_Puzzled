from bge import logic
from challenge_menu_listerners import *
from challenges_list import *
from objproperties import ObjProperties
from navigator import closeLoadingScreen, overlayLoadingScreen
from player import getPlayerId

def init(controller):
    OnStartMenuListingListerner().attach(
        'show_loading_screen', overlayLoadingScreen
    )
    OnStartMenuListingListerner().attach(
        'clear_position_nodes', lambda: clearPositionNodes(scene)
    )
    OnCompleteMenuListListerner.attach(
        'remove_loading_screen', closeLoadingScreen 
    )
    scene = logic.getCurrentScene()
    positionNodes = getPositionNodes(scene)
    paginator = getPaginator(CHALLENGE_LIST, positionNodes)
    setMainCanvas(paginator, positionNodes)
    showChallengeList(CHALLENGE_LIST, positionNodes) 

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

def getPaginator(challenges, positionNodes):
    paginator = ListPaginator('challenges', logic)
    positionNodes.reverse()
    itemsPerPage = len(positionNodes)

    if not paginator.isset():
        paginator.paginate(challenges, itemsPerPage)
    else:
        paginator.load()
    return paginator

def setMainCanvas(paginator, positionNodes):
    canvas = ListCanvas()
    canvas.loadStatic()
    paginator = ListPaginator('challenges', logic)
    nextButton = Button(canvas.nextBtnObj, logic)
    previousButton = Button(canvas.previousBtnObj, logic)
    
    OnChallengeListChangeListerner().attach(
        'update_page_number', 
        lambda index, challenges: Text(canvas.pageNumTxtObj, index + 1)
    )

    OnChallengeListChangeListerner().attach(
        'update_challenge_list',
        lambda index, challenges: showChallengeList(challenges, positionNodes)
    )

    nextButton.setOnClickAction(
        lambda: nextChallengeList(positionNodes)
    )

    previousButton.setOnClickAction(
        lambda: previousChallengeList(positionNodes)
    )
    canvas.fadeIn()

def showChallengeList(challenges, positionNodes):
    OnStartMenuListingListerner.onStart()
    for index, challenge in enumerate(challenges):
        canvas = ChallengeCanvas(index)
        canvas.add(positionNodes[index])
        setChallengeMenu(canvas, challenge)
        canvas.fadeIn()
    OnMenuListComplete().onComplete()

def setChallengeMenu(canvas, challenge):
    playerId = getPlayerId()
    challengeId = getChallengeId(challenge)
    score = Scores(playerId, challengeId)
    scene = logic.getCurrentScene()

    moves = 0
    time = '00:00:00'
    streaks = 0

    if score.isset():
        moves = score.moves
        streaks = score.streaks
        time = frmtTime(score.timeCompleted)

    Text(canvas.titleTxtObj, title)
    Text(canvas.timeTxtObj, time)
    Text(canvas.movesTxtObj, moves)
    Text(canvas.streaksTxtObj, streaks)

    playButton = Button(canvas.playBtnObj, logic)
    challengeViewButton = Button(canvas.patternBtnObj, logic)

    playButton.setOnClickAction(playAction)
    challengeViewButton.setOnClickAction(
        lambda: showChallengeViewer(scene, challenge)
    )


