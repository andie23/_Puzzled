from bge import logic
from navigator import *
from widgets import Text, Button
from canvas import AssessmentCanvas, InitialAssessmentCanvas
from utils import frmtTime, calcPercDiff
from pcache import Scores, Stats
from game import *
from logger import logger

log = logger()

def main():
    benchmark = getBenchmark()
    score = generateScore()

    if benchmark:
        isBenchmark = score < benchmark.overallScore
        setStats(isBenchmark)
        
        if isBenchmark:
             setBenchmark(score)
        return showAssessment(benchmark,{
            'time' : assessTime(benchmark.timeCompleted, getPlayStats('time')),
            'moves' : assessMoves(benchmark.moves, getPlayStats('moves')),
            'streaks' : assessStreaks(benchmark.streaks, getPlayStats('match_streak')),
            'overall_score': assessScore(benchmark.overallScore, score)
        })
    
    setBenchmark(score)
    setStats()
    showInitialDialog()

def setStats(isBenchmark=False):
    stats = Stats(getDefaultUser('id'), getActiveChallenge('id'))
    
    if not stats.fetch():
        stats.playCount = 1
        stats.loses = 0
        stats.wins = 1
        stats.totalTime= getPlayStats('time')
        stats.add()
    else:
        stats.playCount += 1
        stats.totalTime += getPlayStats('time')
        if isBenchmark:
            stats.wins += 1
        else:
            stats.loses +=1
        stats.update()

def setBenchmark(points):
    score = getScoreObj()
    score.timeCompleted = getPlayStats('time')
    score.moves = getPlayStats('moves')
    score.streaks = getPlayStats('match_streak')
    score.overallScore = points

    if score.isset():
        return score.update()
    score.add()

def assessTime(timeBenchmark, time):
    return getPercentageDiffStatus(timeBenchmark, time)

def assessMoves(movesBenchmark, moves):
    return getPercentageDiffStatus(movesBenchmark, moves)

def assessStreaks(streakBenchmark, streaks):
    return getPercentageDiffStatus(streakBenchmark, streaks, '>')

def assessScore(scoreBenchmark, score):
    return getPercentageDiffStatus(scoreBenchmark, score)

def generateScore():
    return getPlayStats('moves') - int(getPlayStats('time')) - getPlayStats('match_streak')

def getScoreObj():
    return Scores(
        pid=getDefaultUser('id'), 
        challenge=getActiveChallenge('id')
    )

def getBenchmark():
    score = getScoreObj()
    if score.fetch():
        return score
    return None

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
        return "%s %% better!!" % assessment['percentage']
    return "%s %% worse!!" % assessment['percentage']

def setCanvas(canvas):
    scene = SceneHelper(logic).getscene('ASSESSMENT')
    if not canvas.isset():
        canvas.add(scene.objects['assessment_position_node'])
    else:
        canvas.load()
    return canvas

def showInitialDialog():
    canvas = setCanvas(InitialAssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)

    Text(canvas.titleTxtObj, getActiveChallenge('name'))
    Text(canvas.currentMovesTxtObj, getPlayStats('moves'))
    Text(canvas.currentTimeTxtObj, frmtTime(getPlayStats('time')))
    Text(canvas.currentStreakTxtObj, getPlayStats('match_streak')) 
    canvas.popIn()
    
def showAssessment(benchmark, assessment):
    canvas = setCanvas(AssessmentCanvas())
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    Text(canvas.titleTxtObj, getActiveChallenge('name'))
    Text(canvas.currentMovesTxtObj, getPlayStats('moves'))
    Text(canvas.currentTimeTxtObj, frmtTime(getPlayStats('time')))
    Text(canvas.currentStreakTxtObj, getPlayStats('match_streak'))   
    Text(canvas.previousTimeTxtObj, frmtTime(benchmark.timeCompleted))
    Text(canvas.previousStreakTxtObj, benchmark.streaks)
    Text(canvas.previousMovesTxtObj, benchmark.moves)
    Text(canvas.timeAssessmentTxtObj, formatAssessment(assessment['time']))
    Text(canvas.movesAssessmentTxtObj, formatAssessment(assessment['moves']))
    Text(canvas.overrallAssessmentTxtObj, formatAssessment(assessment['overall_score']))
    Text(canvas.streakAssessmentTxtObj, formatAssessment(assessment['streaks']))
    if assessment['overall_score']['status'] == 1:
        Text(canvas.statusTxtObj, "You Rock!!")
    else:
        Text(canvas.statusTxtObj, "You Suck!!")
    canvas.fadeIn()
