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
        isBenchmark = score < benchmark['overall_score']
        setStats(isBenchmark)
        
        if isBenchmark:
             saveBenchmark(score)
        return showAssessment(benchmark,{
            'time' : assessTime(benchmark['time'], getPlayStats('time')),
            'moves' : assessMoves(benchmark['moves'], getPlayStats('moves')),
            'streaks' : assessStreaks(benchmark['streaks'], getPlayStats('match_streak')),
            'overall_score': assessScore(benchmark['overall_score'], score)
        })
    
    saveBenchmark(score)
    setStats()
    showInitialDialog()

def setStats(isBenchmark=False):
    stats = Stats(getDefaultUser('id'), getActiveChallenge('id'))
    if not stats.isset():
        stats.add(
            playCount=1, gameovers=0,  wins=1, 
            totalTime=getPlayStats('time') 
        )
    else:
        stats.edit({
            'play_count': stats.get('play_count') + 1,
            'total_time': stats.get('total_time') + getPlayStats('time'),
            'wins': stats.get('wins') + 1 if isBenchmark else stats.get('wins'),
            'gameovers': stats.get('gameovers') + 1 if not isBenchmark else stats.get('gameovers'),
        })

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

def saveBenchmark(overallScore):
    score = getScoreObj()
 
    if score.isset():
        score.editOverallScore(overallScore)
        score.editTime(getPlayStats('time'))
        score.editMoves(getPlayStats('moves'))
        score.editStreaks(getPlayStats('match_streak'))
    else:
        score.add(
            getPlayStats('time'), 
            getPlayStats('moves'), 
            getPlayStats('match_streak'),
            overallScore
        )

def getScoreObj():
    return Scores(
        pid=getDefaultUser('id'), 
        challenge=getActiveChallenge('id')
    )

def getBenchmark():
    score = getScoreObj()
    if score.isset():
        return {
            'moves' : score.moves,
            'streaks' : score.streaks,
            'overall_score' : score.overallScore,
            'time' : score.timeCompleted
        }
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
    Text(canvas.previousTimeTxtObj, frmtTime(benchmark['time']))
    Text(canvas.previousStreakTxtObj, benchmark['streaks'])
    Text(canvas.previousMovesTxtObj, benchmark['moves'])
    Text(canvas.timeAssessmentTxtObj, formatAssessment(assessment['time']))
    Text(canvas.movesAssessmentTxtObj, formatAssessment(assessment['moves']))
    Text(canvas.overrallAssessmentTxtObj, formatAssessment(assessment['overall_score']))
    Text(canvas.streakAssessmentTxtObj, formatAssessment(assessment['streaks']))
    if assessment['overall_score']['status'] == 1:
        Text(canvas.statusTxtObj, "You Rock!!")
    else:
        Text(canvas.statusTxtObj, "You Suck!!")
    canvas.fadeIn()
