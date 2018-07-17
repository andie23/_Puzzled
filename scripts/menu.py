from widgets import ChallengeCanvas, ButtonWidget
from psetup import PSETUPS
from pcache import Scores
from bge import logic
from objproperties import ObjProperties
from utils import DictPaginator, frmtTime
from logger import logger

def challengesMain():    
    gdict = logic.globalDict
    challengeList = PSETUPS
    scene = logic.getCurrentScene()
    objProps = ObjProperties()
    positionNodes = objProps.getPropObjGroup('canvas_position', scene)
    totalItemsPerPage = len(positionNodes)
    paginator = DictPaginator('challenges', logic)

    if not paginator.isset():
        paginator.paginate(challengeList, totalItemsPerPage)
    else:
        paginator.load()

    challengeGroup = paginator.get()
    _listChallenges(challengeGroup, positionNodes)

    nextBtn = ButtonWidget(scene.objects['btn_next'], logic)
    nextBtn.setCommand(
        _nextChallengeList, 'challenges', positionNodes
    )

    prevBtn = ButtonWidget(scene.objects['btn_previous'], logic)
    prevBtn.setCommand(
        _prevChallengeList, 'challenges',positionNodes
    )

def _removeCanvasList():
    objProps = ObjProperties()
    scene = logic.getCurrentScene()
    canvasList = objProps.getPropObjGroup('canvasID', scene)
    for canvas in canvasList:
        canvas.endObject()

def _startChallenge(setup):
    scene = logic.getCurrentScene()
    logic.globalDict['gsetup'] = setup
    scene.replace('MAIN')

def _nextChallengeList(paginatorID, positionNodes):
    paginator = DictPaginator(paginatorID, logic)
    if paginator.isset():
        _removeCanvasList()
        paginator.load()
        paginator.next()
        _listChallenges(paginator.get(), positionNodes)

def _prevChallengeList(paginatorID, positionNodes):
    paginator = DictPaginator(paginatorID, logic)

    if paginator.isset():
        _removeCanvasList()
        paginator.load()
        paginator.previous()
        _listChallenges(paginator.get(), positionNodes)

def _listChallenges(challengeGroup, positionNodes):
    playerID = logic.globalDict['player']['id']
    canvas = ChallengeCanvas(logic)
    groupIndex = 0
    
    for cheader, cbody in challengeGroup.items():
        challengeID = '%s_%s' % (
            cbody['pattern'], cbody['eventScript']
        )

        score = Scores(playerID, challengeID)
        canvasPosition = positionNodes[groupIndex]
        canvas.add(cheader, canvasPosition)
        canvas.setTitleTxt(cheader)
        canvas.setTimeTxt('N/A')
        canvas.setMovesTxt('N/A')
        canvas.setPlayBtn(_startChallenge, cbody)

        if score.isset():
            canvas.setTimeTxt(frmtTime(score.timeCompleted))
            canvas.setMovesTxt(score.moves)
        
        groupIndex += 1
