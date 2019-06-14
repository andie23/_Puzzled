from bge import logic
from assessment_calculation import *
from text_widget import Text
from button_widget import Button
from assessment_canvas import AssessmentCanvas
from initial_assessment_canvas import InitialAssessmentCanvas
from canvas_effects import fadeIn, dialogPopIn
from game_event_listerners import OnPuzzleRestartListerner

def init(controller):
    from player import getPlayerId
    from session_global_data import SessionGlobalData
    from challenge_global_data import LoadedChallengeGlobalData

    OnPuzzleRestartListerner().attach('remove_self', controller.owner.endObject)

    runAssessment(
        getPlayerId(), SessionGlobalData(),
        LoadedChallengeGlobalData()
    )

def runAssessment(playerId, playSession, loadedChallenge):
    challengeId = loadedChallenge.getId()
    challengeName = loadedChallenge.getName()
    moves = playSession.getMoves()
    time = playSession.getTime()
    streaks = playSession.getBenchmarkStreakCount()
    curScore = calculateScore(moves, time, streaks)
    benchmark = getBenchmark(playerId, challengeId)

    if benchmark:
        if curScore < benchmark.overallScore:
            updateChallengeStats(playerId, challengeId, time, True)
            updateChallengeBenchmark(playerId, challengeId, moves, time, streaks, curScore)
        
        showAssessmentCanvas(challengeName, {
            'prev_time' : benchmark.timeCompleted,
            'prev_moves' : benchmark.moves,
            'prev_streaks' : benchmark.streaks,
            'cur_time': time,
            'cur_moves': moves,
            'cur_streaks' : streaks,
            'time_assessment' : assessTime(benchmark.timeCompleted, time),
            'moves_assessment' : assessMoves(benchmark.moves, moves),
            'streaks_assessment' : assessStreaks(benchmark.streaks, streaks),
            'overall_assessment' : assessScore(benchmark.overallScore, curScore)
        })
    else:
        addChallengeBenchmark(playerId, challengeId, moves, time, streaks, curScore)
        updateChallengeStats(playerId, challengeId, time)
        showInformationCanvas(challengeName, time, moves, streaks)

def setCanvas(canvas, isVisible=True):
    from scene_helper import Scene
    

    scene = Scene('HUD').getscene()
    if not canvas.isset():
        canvas.add(scene.objects['information_position_node'], isVisible)
   
    OnPuzzleRestartListerner().attach(
        'remove_assessment_canvas', canvas.remove
    )
    return canvas

def showInformationCanvas(challengeName, time, moves, streaks):
    from game import reshuffle, quit

    canvas = setCanvas(InitialAssessmentCanvas(), False)
    reshuffleBtn = Button(canvas.reshuffleBtnObj)
    exitBtn = Button(canvas.exitBtnObj)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)

    Text(canvas.titleTxtObj, challengeName, limit=18)
    Text(canvas.currentMovesTxtObj, moves)
    Text(canvas.currentTimeTxtObj, frmtTime(time))
    Text(canvas.currentStreakTxtObj, streaks) 
    canvas.show()
    #dialogPopIn(canvas, onFinishAction=canvas.resetPosition)
    
def showAssessmentCanvas(challengeName, data):
    from game import reshuffle, quit
    
    canvas = setCanvas(AssessmentCanvas(), False)
    reshuffleBtn = Button(canvas.reshuffleBtnObj)
    exitBtn = Button(canvas.exitBtnObj)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    Text(canvas.titleTxtObj, challengeName, limit=18)
    Text(canvas.currentMovesTxtObj, data['cur_moves'])
    Text(canvas.currentTimeTxtObj, frmtTime(data['cur_time']))
    Text(canvas.currentStreakTxtObj, data['cur_streaks'])   
    Text(canvas.previousTimeTxtObj, frmtTime(data['prev_time']))
    Text(canvas.previousStreakTxtObj, data['prev_streaks'])
    Text(canvas.previousMovesTxtObj, data['prev_moves'])
    Text(canvas.timeAssessmentTxtObj, formatAssessment(data['time_assessment']))
    Text(canvas.movesAssessmentTxtObj, formatAssessment(data['moves_assessment']))
    Text(canvas.overrallAssessmentTxtObj, formatAssessment(data['overall_assessment']))
    Text(canvas.streakAssessmentTxtObj, formatAssessment(data['streaks_assessment']))
    if data['overall_assessment']['status'] == 1:
        Text(canvas.statusTxtObj, "You Rock!!")
    else:
        Text(canvas.statusTxtObj, "You Suck!!")
    canvas.show()
    #dialogPopIn(canvas, onFinishAction=canvas.resetPosition)
