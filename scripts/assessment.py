from bge import logic
from widgets import Text, Button
from canvas import AssessmentCanvas
from utils import frmtTime, calcPercDiff
from pcache import Scores
from game import *
from logger import logger

log = logger()

def assessMainBenchmarkScore():
    gdict = logic.globalDict
    gsetup = gdict['gsetup']
    benchmark = gsetup['benchmark']
    session = getSession()

    return {
        'input_benchmark': evaluateInputChallenge(session, benchmark),
        'score_benchmark' : evaluateTargetScore(session, benchmark)
    }
    
def evaluateTargetScore(session, benchmarks):
    assessment = {}
    rangedValues = ['time', 'moves', 'chain_count']
    
    for varType, data in benchmarks.items():
        if varType not in rangedValues:
            continue

        curscore= session[varType]
        assessment[varType] = None

        minval = data['min']
        maxval = data['max']

        if curscore <= minval:
            assessment[varType] = {
                'requirement': minval, 
                'result': curscore,
                'status': 'pass'
            }
        elif curscore >= minval and curscore <= maxval:
            assessment[varType] = {
                'requirement' : maxval,
                'result': curscore,
                'status': 'pass'
            }
    return assessment
          
def evaluateInputChallenge(session, benchmark):
    if 'input' not in benchmark:
        return
    
    inputTypes = ['mouse', 'keyboard', 'keyboard+mouse']
    inputBenchmark = benchmark['input']
    usedInputDevice = session['input']
    assessment = {}
    
    if usedInputDevice in inputBenchmark:
        assessment = {
            'requirement' : usedInputDevice,
            'result': usedInputDevice,
            'status': 'pass'
        }

        inputBenchmarkVals = inputBenchmark[usedInputDevice]
        if inputBenchmarkVals:
            assessment.update({
                'value_benchmarks' : evaluateTargetScore(
                    session, inputBenchmarkVals
                ) 
        })
    return assessment

def main(controller):
    log.debug(assessMainBenchmarkScore())
    session = getSession()
    gdict = logic.globalDict
    gsetup = gdict['GameSetup']
    
    playerID = gdict['player']['id']
    challengeID = gsetup['id']
    challengeTitle = gsetup['name']

    curTime = session['time']
    curMoves = session['moves']
    assessment = getAssessmentDefaults()
    assessment.update({
        'title': challengeTitle, 
        'cur_time': frmtTime(curTime), 
        'cur_moves':curMoves
    })
    
    score = Scores(pid=playerID, challenge=challengeID)

    if score.isset():
       prevMoves = score.moves
       prevTime = score.timeCompleted
       assessment.update({
            'prev_time': frmtTime(prevTime), 
            'prev_moves': prevMoves
        })
       perfomance = calculatePerfomance(
            prevTime, prevMoves, curTime, curMoves
       )
       assessment.update(frmtPerfomanceData(perfomance))
       
       if perfomance['overrall_score']['status'] == 1:
           score.editTime(curTime)
           score.editMoves(curMoves)
           assessment.update({'status': 'New benchmark set!'})
    else:
        score.add(curTime, curMoves)
        assessment.update({'status': 'New benchmark set!'})

    showAssessment(assessment)

def getAssessmentDefaults():
    return {
        'title': 'None',
        'status': ':(', 
        'cur_time': '00:00:00.0', 
        'cur_moves': 0, 
        'prev_time': 'N/A',
        'prev_moves': 'N/A', 
        'time_score': 'N/A',
        'moves_score': 'N/A', 
        'overrall_score': 'N/A'
    }

def calculatePerfomance(prevTime, prevMoves, curTime, curMoves):
    prevScore = prevTime + prevMoves
    curScore = curTime + curMoves

    timeAssessment = assess(curTime, prevTime)
    movesAssessment = assess(curMoves, prevMoves)
    scoreAssessment = assess(curScore, prevScore)

    return {
        'time_score' : timeAssessment, 
        'moves_score': movesAssessment,
        'overrall_score' : scoreAssessment
    }

def frmtPerfomanceData(data):
    build = {}
    for header, body in data.items():
        status = body['status']
        percentage = body['percentage']
        build[header] = '{0}% {1}'.format(
            percentage, 'Better' if status == 1 else 'Worse!!'
        )
    return build

def assess(curVal, prevVal):
    if curVal < prevVal:
       percDiff =  calcPercDiff(prevVal, curVal)
       return {'status': 1, 'percentage': percDiff}
    percDiff = calcPercDiff(curVal, prevVal)
    return {'status': 0, 'percentage': percDiff}

def showAssessment(data):
    canvas = AssessmentCanvas(logic)
    canvas.load('assessement')
    reshuffleBtn = Button(canvas.reshuffleBtnObj, logic)
    exitBtn = Button(canvas.exitBtnObj, logic)

    reshuffleBtn.setOnclickAction(reshuffle)
    exitBtn.setOnclickAction(quit)
    
    Text(canvas.titleTxtObj, data['title'])
    Text(canvas.currentMovesTxtObj, data['cur_moves'])
    Text(canvas.currentTimeTxtObj, data['cur_time'])
    Text(canvas.previousTimeTxtObj, data['prev_time'])
    Text(canvas.previousMovesTxtObj, data['prev_moves'])
    Text(canvas.timeAssessmentTxtObj, data['time_score'])
    Text(canvas.movesAssessmentTxtObj, data['moves_score'])
    Text(canvas.overrallAssessmentTxtObj, data['overrall_score'])
    Text(canvas.statusTxtObj, data['status'])
    