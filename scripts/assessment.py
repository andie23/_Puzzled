from bge import logic
from navigator import *
from widgets import Text, Button
from canvas import AssessmentCanvas, InitialAssessmentCanvas
from utils import frmtTime, calcPercDiff
from pcache import Scores
from game import *
from logger import logger

log = logger()

def main():
    achievement = getSession()
    pId = getPlayerId()
    challenge = getChallengeId()
    benchmark = getBenchmark(pId, challenge)

    score = generateScore(achievement)
    
    if benchmark:
        if score < benchmark.overallScore:
            saveBenchmark(pId, challenge, achievement, score)
        return showAssessment(benchmark, achievement, {
            'time' : assessTime(benchmark.timeCompleted, achievement['time']),
            'moves' : assessMoves(benchmark.moves, achievement['moves']),
            'streaks' : assessStreaks(benchmark.streaks, achievement['chain_count']),
            'overall_score': assessScore(benchmark.overallScore, score)
        })
    
    saveBenchmark(pId, challenge, achievement, score)
    showInitialDialog(achievement)

def assessTime(timeBenchmark, time):
    return getPercentageDiffStatus(timeBenchmark, time)

def assessMoves(movesBenchmark, moves):
    return getPercentageDiffStatus(movesBenchmark, moves)

def assessStreaks(streakBenchmark, streaks):
    return getPercentageDiffStatus(streakBenchmark, streaks, '>')

def assessScore(scoreBenchmark, score):
    return getPercentageDiffStatus(scoreBenchmark, score)

def generateScore(achievement):
    return achievement['moves'] - int(achievement['time']) - achievement['chain_count']

def saveBenchmark(pId, challenge, achievement, overallScore):
    score = Scores(pid=pId, challenge=challenge)
    if score.isset():
        score.editOverallScore(overallScore)
        score.editTime(achievement['time'])
        score.editMoves(achievement['moves'])
        score.editStreaks(achievement['chain_count'])
    else:
        score.add(
            achievement['time'], 
            achievement['moves'], 
            achievement['chain_count'],
            overallScore
        )

def getBenchmark(pId, challenge):
    score = Scores(pid=pId, challenge=challenge)
    if score.isset():
        return score
    return None

def getPlayerId():
    return logic.globalDict['player']['id']

def getChallengeId():
    return logic.globalDict['GameSetup']['id']

def getChallengeTitle():
    return logic.globalDict['GameSetup']['name']

def getPercentageDiffStatus(benchmark, achievement, statusPassCondition='<'):
    status = 0
    if statusPassCondition == '<':
        if achievement < benchmark:
            diff = calcPercDiff(benchmark, achievement)
            status = 1
        else:
            diff = calcPercDiff(achievement, benchmark)
    
    if statusPassCondition == '>':
        if achievement > benchmark:
            diff = calcPercDiff(achievement, benchmark)
            status = 1
        else:
            diff = calcPercDiff(benchmark, achievement)
  
    return { 'status': status, 'percentage': diff}

def formatAssessment(assessment):     
    if assessment['status'] == 1:
        return "%s better!!" % assessment['percentage']
    return "%s worse!!" % assessment['percentage']

def setCanvas(canvas):
    scene = SceneHelper(logic).getscene('ASSESSMENT')
    if not canvas.isset():
        canvas.add(scene.objects['assessment_position_node'])
    else:
        canvas.load()
    return canvas

def showInitialDialog(achievement):
    canvas = setCanvas(InitialAssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)

    Text(canvas.currentMovesTxtObj, achievement['moves'])
    Text(canvas.currentTimeTxtObj, achievement['time'])
    Text(canvas.currentStreakTxtObj, achievement['chain_count']) 
    canvas.popIn()
    
def showAssessment(benchmark, achievement, assessment):
    canvas = setCanvas(AssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    Text(canvas.titleTxtObj, getChallengeTitle())
    Text(canvas.currentMovesTxtObj, achievement['moves'])
    Text(canvas.currentTimeTxtObj, achievement['time'])
    Text(canvas.currentStreakTxtObj, achievement['chain_count'])    
    Text(canvas.previousTimeTxtObj, benchmark.timeCompleted)
    Text(canvas.previousStreakTxtObj, benchmark.streaks)
    Text(canvas.previousMovesTxtObj, benchmark.moves)
    Text(canvas.timeAssessmentTxtObj, formatAssessment(assessment['time']))
    Text(canvas.movesAssessmentTxtObj, formatAssessment(assessment['moves']))
    Text(canvas.overrallAssessmentTxtObj, formatAssessment(assessment['overall_score']))
    Text(canvas.streakAssessmentTxtObj, formatAssessment(assessment['streaks']))
    if assessment['overall_score']['status'] == 1:
        Text(canvas.statusTxtObj, "You Rock!!")
    else:
        Text(canvas.statusTxtObj, "You suck!!")
    canvas.fadeIn()
