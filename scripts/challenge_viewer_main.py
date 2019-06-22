from bge import logic
from utils import frmtTime

def init():
    from player import getPlayerId
    from challenge_global_data import LoadedChallengeGlobalData

    challengeData = LoadedChallengeGlobalData()
    menu = addChallengeViewer(challengeData.getPattern())
    setBenchmarkMenu(
        menu, getPlayerId(),
        challengeData.getName(),
        challengeData.getId()
    )
    menu.open()

def addChallengeViewer(pattern):
    from scene_helper import Scene
    from objproperties import ObjProperties
    from pattern_loader import PatternLoader
    from challenge_viewer_canvas import ChallengeViewerCanvas
    from menu import PopUpMenu, CENTER_POSITION_NODE

    menu = PopUpMenu(ChallengeViewerCanvas(), CENTER_POSITION_NODE)
    PatternLoader(Scene('HUD').getscene(), pattern).load()
    return menu

def setBenchmarkMenu(menu, playerId, challengeName, challengeId):
    from pcache import Stats, Scores
    from puzzle_main import startPuzzleScene
    from button_widget import Button
    from text_widget import Text

    score = Scores(playerId, challengeId)
    stats = Stats(playerId, challengeId)

    playBtn = Button(menu.canvas.playBtnObj)
    returnBtn = Button(menu.canvas.exitBtnObj)

    returnBtn.setOnclickAction(menu.close)
    playBtn.setOnclickAction(lambda: menu.close(startPuzzleScene))

    Text(menu.canvas.titleTxtObj, challengeName)
    if score.fetch():
        Text(menu.canvas.timeTxtObj, frmtTime(score.timeCompleted))
        Text(menu.canvas.movesTxtObj, score.moves)
        Text(menu.canvas.streakCountTxtObj, score.streaks)

    if stats.fetch():
        Text(menu.canvas.playCountTxtObj, stats.playCount)
        Text(menu.canvas.playTimeTxtObj, frmtTime(stats.totalTime))
        Text(menu.canvas.winsTxtObj, stats.wins)
        Text(menu.canvas.losesTxtObj, stats.loses)


