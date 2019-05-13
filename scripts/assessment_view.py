from bge import logic
from assessment_calculation import *
from navigator import *
from widgets import Text, Button
from canvas import AssessmentCanvas, InitialAssessmentCanvas
from global_dictionary import PuzzleSessionGlobalData, LoadedChallengeGlobalData
from game_event_listerners import OnPuzzleExitListerner, OnPuzzleRestartListerner
from player import getPlayerId

def init(controller):
    OnPuzzleExitListerner().attach(
        'close_assessment_view', closeAssessmentScreen
    )
    OnPuzzleRestartListerner().attach(
        'close_assessment_view', closeAssessmentScreen
    )
    loadedChallenge = LoadedChallengeGlobalData()
    playSession = PuzzleSessionGlobalData()
    runAssessment(getPlayerId(), playSession, loadedChallenge)

def runAssessment(playerId, playSession, loadedChallenge):
    challengeId = loadedChallenge.getId()
    challengeName = loadedChallenge.name
    moves = playSession.moves
    time = playSession.time
    streaks = playSession.streakCount
    curScore = calculateScore(moves, time, streaks)

    prevScore = getPrevScore(playerId, challengeId)

    if prevScore:
        if curScore < prevScore.overallScore:
            updateChallengeStats(playerId, time, True)
            updateChallengeBenchmark(playerId, challengeId, moves, time, streaks)

        showAssessmentCanvas(challengeName, {
            'prev_time' : prevScore.timeCompleted,
            'prev_moves' : prevScore.moves,
            'prev_streaks' : prevScore.streaks
            'cur_time': time,
            'cur_moves': moves,
            'cur_streaks' : streaks,
            'time_assessment' : assessTime(prevScore.timeCompleted, time),
            'moves_assessment' : assessMoves(prevScore.moves, moves),
            'streaks_assessment' : assessStreaks(prevScore.streaks, streaks),
            'overall_assessment' : assessScore(prevScore.overallScore, curScoreAvg)
        })
    else:
        addChallengeBenchmark(playerId, challengeId, moves, time, streaks )
        updateChallengeStats(playerId, challengeId, time)
        showInformationCanvas(loadedChallengeName, time, moves, streaks)

def setCanvas(canvas):
    scene = SceneHelper(logic).getscene('ASSESSMENT')
    if not canvas.isset():
        canvas.add(scene.objects['assessment_position_node'])
    else:
        canvas.load()
    return canvas

def showInformationCanvas(challengeName, moves, time, streaks):
    canvas = setCanvas(InitialAssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)

    Text(canvas.titleTxtObj, challengeName)
    Text(canvas.currentMovesTxtObj, moves)
    Text(canvas.currentTimeTxtObj, frmtTime(time))
    Text(canvas.currentStreakTxtObj, streaks) 
    canvas.fadeIn()
    
def showAssessmentCanvas(challengeName, data):
    canvas = setCanvas(AssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    Text(canvas.titleTxtObj, challengeName)
    Text(canvas.currentMovesTxtObj, data['cur_moves'])
    Text(canvas.currentTimeTxtObj, frmtTime(data['cur_time']))
    Text(canvas.currentStreakTxtObj, data['cur_streaks'])   
    Text(canvas.previousTimeTxtObj, frmtTime(data['prev_time']))
    Text(canvas.previousStreakTxtObj, data['prev_streaks'])
    Text(canvas.previousMovesTxtObj, data['prev_moves'])
    Text(canvas.timeAssessmentTxtObj, formatAssessment(assessment['time_assessment']))
    Text(canvas.movesAssessmentTxtObj, formatAssessment(assessment['moves_assessment']))
    Text(canvas.overrallAssessmentTxtObj, formatAssessment(assessment['overall_score']))
    Text(canvas.streakAssessmentTxtObj, formatAssessment(assessment['streak_assessment']))
    if assessment['overall_score']['status'] == 1:
        Text(canvas.statusTxtObj, "You Rock!!")
    else:
        Text(canvas.statusTxtObj, "You Suck!!")
    canvas.fadeIn()
