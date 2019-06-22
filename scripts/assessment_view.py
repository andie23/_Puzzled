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

def getPopupMenu(canvas):
    from menu import PopUpMenu, CENTER_POSITION_NODE
    from game import reshuffle, quit
    
    menu = PopUpMenu(canvas, CENTER_POSITION_NODE)

    reshuffleBtn = Button(menu.canvas.reshuffleBtnObj)
    exitBtn = Button(menu.canvas.exitBtnObj)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    OnPuzzleRestartListerner().attach(
        'remove_assessment_canvas', menu.close
    )
    return menu

def showInformationCanvas(challengeName, time, moves, streaks):
    menu = getPopupMenu(InitialAssessmentCanvas())    
    Text(menu.canvas.titleTxtObj, challengeName, limit=18)
    Text(menu.canvas.currentMovesTxtObj, moves)
    Text(menu.canvas.currentTimeTxtObj, frmtTime(time))
    Text(menu.canvas.currentStreakTxtObj, streaks) 
    menu.open()

def showAssessmentCanvas(challengeName, data):
    menu = getPopupMenu(AssessmentCanvas())    
    Text(menu.canvas.titleTxtObj, challengeName, limit=18)
    Text(menu.canvas.currentMovesTxtObj, data['cur_moves'])
    Text(menu.canvas.currentTimeTxtObj, frmtTime(data['cur_time']))
    Text(menu.canvas.currentStreakTxtObj, data['cur_streaks'])   
    Text(menu.canvas.previousTimeTxtObj, frmtTime(data['prev_time']))
    Text(menu.canvas.previousStreakTxtObj, data['prev_streaks'])
    Text(menu.canvas.previousMovesTxtObj, data['prev_moves'])
    Text(menu.canvas.timeAssessmentTxtObj, formatAssessment(data['time_assessment']))
    Text(menu.canvas.movesAssessmentTxtObj, formatAssessment(data['moves_assessment']))
    Text(menu.canvas.overrallAssessmentTxtObj, formatAssessment(data['overall_assessment']))
    Text(menu.canvas.streakAssessmentTxtObj, formatAssessment(data['streaks_assessment']))
    if data['overall_assessment']['status'] == 1:
        Text(menu.canvas.statusTxtObj, "You Rock!!")
    else:
        Text(menu.canvas.statusTxtObj, "You Suck!!")

    menu.open()
