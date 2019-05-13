from bge import logic
from widgets import Button, Text
from canvas import PatternCanvas
from navigator import overlayChallengeView, closePatternScreen
from pcache import Stats, Scores
from utils import frmtTime
from player import getPlayerId
from puzzle_main import startPuzzleScene
from pattern_visualiser import PatternVisualiser

def init(controller):
    challengeData = LoadedChallengeGlobalData()
    playerId = getPlayerId()
    # show player scores and stats
    setScoreCanvas(playerId, challengeData)
    # show visual representation of how to order puzzle blocks
    PatternVisualiser().visualise(challengeData.getPattern())

def startChallengeViewerScene(challenge):
    LoadedChallengeGlobData().set(challenge)
    overlayChallengeView()

def setScoreCanvas(playerId, challenge):
    challengeId = challenge.getId()
    score = Scores(playerId, challengeId)
    stats = Stats(playerId, challengeId)
    pcanvas = PatternCanvas()
    pcanvas.loadStatic()
    
    playBtn = Button(pcanvas.playBtnObj, logic)
    playBtn.setOnclickAction(lambda: startPuzzleScene(challenge))
    
    returnBtn = Button(pcanvas.backBtnObj, logic)
    returnBtn.setOnclickAction(closePatternScreen)
    Text(pcanvas.titleTxtObj, challenge.name)

    if score.fetch():
        Text(pcanvas.prevTimeTxtObj, frmtTime(score.timeCompleted))
        Text(pcanvas.prevMovesTxtObj, score.moves)
        Text(pcanvas.prevStreakTxtObj, score.streaks)

    if stats.fetch():
        Text(pcanvas.playCountTxtObj, stats.playCount)
        Text(pcanvas.playTimeTxtObj, frmtTime(stats.totalTime))
        Text(pcanvas.winsTxtObj, stats.wins)
        Text(pcanvas.losesTxtObj, stats.loses)

