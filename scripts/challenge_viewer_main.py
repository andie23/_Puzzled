from bge import logic
from utils import frmtTime
from scene_helper import Scene

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
    animateVisualBlocks(challengeData.getId(), menu)

def addChallengeViewer(pattern):
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

def animateVisualBlocks(challengeName, menu, timerDelay=0.3):
    from block_effects import animate_match_color
    from objproperties import ObjProperties
    from timer import Timer
    
    id = 'pattern_visualiser_data'
    scene = Scene('HUD').getscene()

    if id not in logic.globalDict:
        logic.globalDict[id] = {
            'total': len(
                ObjProperties().getPropObjGroup('visual_block', scene)
            ), 
            'index': 0 
        }
    else:
        logic.globalDict[id]['index'] = 0

    def markVisualBlocks():
        data = logic.globalDict[id]
        data['index'] += 1
        if data['index'] <= data['total']:
            vsBlock = ObjProperties().getObjByPropVal(
                'visual_block', data['index'], scene.objects
            )
            if vsBlock:
                timer = Timer(id, 'HUD')
                timer.setTimer(
                    timerDelay, lambda: animate_match_color(
                       vsBlock, onfinishAction=markVisualBlocks
                    )  
                )
                timer.start()
        else:
            logic.globalDict[id]['index'] = 0

    markVisualBlocks()

