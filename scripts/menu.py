from widgets import Button, Text
from canvas import ChallengeCanvas, ListCanvas
from challenges import CHALLENGE_LIST
from pcache import Scores
from bge import logic
from objproperties import ObjProperties
from utils import ListPaginator, frmtTime
from logger import logger

def challengesMain():    
    gdict = logic.globalDict
    challengeList = CHALLENGE_LIST
    scene = logic.getCurrentScene()
    paginator = ListPaginator('challenges', logic)
    positionNodes = ObjProperties().getPropObjGroup(
        'canvas_position', scene
    )
    positionNodes.reverse()
    listCanvas = _listCanvas(positionNodes)
    perPage = len(positionNodes)

    if not paginator.isset():
        paginator.paginate(challengeList, perPage)
    else:
        paginator.load()

    challengeGroup = paginator.get()
    _listChallenges(challengeGroup, positionNodes)

def _removeCanvasList():
    objProps = ObjProperties()
    scene = logic.getCurrentScene()
    canvasList = objProps.getPropObjGroup('canvas_id', scene)
    for canvas in canvasList:
        if not ObjProperties(canvas).getProp('canvas_id') == 'list_canvas':
            canvas.endObject()

def _startChallenge(setup):
    scene = logic.getCurrentScene()
    logic.globalDict['gsetup'] = setup
    scene.replace('MAIN')

def _showPattern(setup):
    logic.globalDict['setup_to_visualise'] = setup
    logic.addScene('PATTERN_VIEW', 1)

def _nextChallengeList(paginatorID, positionNodes):
    paginator = ListPaginator(paginatorID, logic)
    if paginator.isset():
        _removeCanvasList()
        paginator.load()
        paginator.next()
        _listChallenges(paginator.get(), positionNodes)

def _prevChallengeList(paginatorID, positionNodes):
    paginator = ListPaginator(paginatorID, logic)

    if paginator.isset():
        _removeCanvasList()
        paginator.load()
        paginator.previous()
        _listChallenges(paginator.get(), positionNodes)

def _listCanvas(positionNodes):
    scene = logic.getCurrentScene()
    canvasPositionNode = scene.objects['main_position_node']

    listCanvas = ListCanvas(logic)
    listCanvas.add('list_canvas', canvasPositionNode)
    
    title = Text(listCanvas.titleTxtObj, 'Challenges')
    nextBtn = Button(listCanvas.nextBtnObj, logic)
    prevBtn = Button(listCanvas.previousBtnObj, logic)

    nextBtn.setOnclickAction(_nextChallengeList, 'challenges', positionNodes)
    prevBtn.setOnclickAction(_prevChallengeList, 'challenges', positionNodes)

def _listChallenges(challengeGroup, positionNodes):
    playerID = logic.globalDict['player']['id']
    canvas = ChallengeCanvas(logic)

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
        playBtn.setOnclickAction(_startChallenge, cbody)

        patBtn = Button(canvas.patternBtnObj, logic)
        patBtn.setOnclickAction(_showPattern, cbody)

        if score.isset():
            Text(canvas.timeTxtObj, frmtTime(score.timeCompleted))
            Text(canvas.movesTxtObj, score.moves)
            Text(canvas.statusTxtObj, 'Complete')
        else:
            Text(canvas.timeTxtObj, 'N/A')
            Text(canvas.movesTxtObj, 'N/A')
            Text(canvas.statusTxtObj, 'unplayed')
