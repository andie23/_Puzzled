from bge import logic
from canvas import PatternCanvas
from navigator import closePatternScreen
from pcache import Stats, Scores
from utils import frmtTime
from player import getPlayerId
from pattern_visualiser import PatternVisualiser

def init():
    from challenge_global_data import LoadedChallengeGlobalData

    challengeData = LoadedChallengeGlobalData()
    playerId = getPlayerId()
    setScoreCanvas(playerId, challengeData.getName, challengeData.getId())
    # start visualiser to mark block in a specific pattern
    PatternVisualiser(logic).visualise(challengeData.getPattern())

def setScoreCanvas(playerId, challengeName, challengeId):
    from puzzle_main import startPuzzleScene
    from button_widget import Button
    from text_widget import Text

    score = Scores(playerId, challengeId)
    stats = Stats(playerId, challengeId)
    pcanvas = PatternCanvas()
    pcanvas.loadStatic()
    
    playBtn = Button(pcanvas.playBtnObj)
    playBtn.setOnclickAction(lambda: startPuzzleScene())
    
    returnBtn = Button(pcanvas.backBtnObj)
    returnBtn.setOnclickAction(closePatternScreen)
    Text(pcanvas.titleTxtObj, challengeName)

    if score.fetch():
        Text(pcanvas.prevTimeTxtObj, frmtTime(score.timeCompleted))
        Text(pcanvas.prevMovesTxtObj, score.moves)
        Text(pcanvas.prevStreakTxtObj, score.streaks)

    if stats.fetch():
        Text(pcanvas.playCountTxtObj, stats.playCount)
        Text(pcanvas.playTimeTxtObj, frmtTime(stats.totalTime))
        Text(pcanvas.winsTxtObj, stats.wins)
        Text(pcanvas.losesTxtObj, stats.loses)

