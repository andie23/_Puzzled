from bge import logic
from challenge_viewer_canvas import ChallengeViewerCanvas
from pcache import Stats, Scores
from utils import frmtTime
from player import getPlayerId
from pattern_loader import PatternLoader
from challenge_global_data import LoadedChallengeGlobalData
from challenge_viewer_canvas import ChallengeViewerCanvas
from scene_helper import Scene
from ui_background import attach_background_object

def init():
    from challenge_global_data import LoadedChallengeGlobalData

    canvas = addChallengeViewer(
        Scene('HUD').getscene(), LoadedChallengeGlobalData().getPattern()
    )
    challengeData = LoadedChallengeGlobalData()
    setScoreCanvas(canvas, getPlayerId(), challengeData.getName(), challengeData.getId())

    
def addChallengeViewer(scene, pattern):
    from objproperties import ObjProperties

    canvas = ChallengeViewerCanvas()
    canvas.add(scene.objects['information_position_node'])
    PatternLoader(scene, pattern).load()
    return canvas

@attach_background_object
def setScoreCanvas(pcanvas, playerId, challengeName, challengeId):
    from puzzle_main import startPuzzleScene
    from button_widget import Button
    from text_widget import Text
    
    def onPlay():
        startPuzzleScene()
        pcanvas.remove()

    score = Scores(playerId, challengeId)
    stats = Stats(playerId, challengeId)

    playBtn = Button(pcanvas.playBtnObj)
    playBtn.setOnclickAction(onPlay)
    
    returnBtn = Button(pcanvas.exitBtnObj)
    returnBtn.setOnclickAction(pcanvas.remove)
    Text(pcanvas.titleTxtObj, challengeName)

    if score.fetch():
        Text(pcanvas.timeTxtObj, frmtTime(score.timeCompleted))
        Text(pcanvas.movesTxtObj, score.moves)
        Text(pcanvas.streakCountTxtObj, score.streaks)

    if stats.fetch():
        Text(pcanvas.playCountTxtObj, stats.playCount)
        Text(pcanvas.playTimeTxtObj, frmtTime(stats.totalTime))
        Text(pcanvas.winsTxtObj, stats.wins)
        Text(pcanvas.losesTxtObj, stats.loses)
    
    return pcanvas

