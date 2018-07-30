from bge import logic
from widgets import Text
from canvas import AssessmentCanvas
from utils import frmtTime, calcPercDiff
from pcache import Scores 

def main(controller):
    gdict = logic.globalDict
    if not 'play_session' in gdict:
        return

    session = gdict['play_session']
    gsetup = gdict['GameSetup']
    playerID = gdict['player']['id']
    challengeID = gsetup['id']
    challengeTitle = gsetup['name']

    curTime = session['current_time']
    curMoves = session['current_moves']

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
    prevScore = int(prevTime) + int(prevMoves)
    curScore = int(curTime) + int(curMoves)

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
    Text(canvas.titleTxtObj, data['title'])
    Text(canvas.currentMovesTxtObj, data['cur_moves'])
    Text(canvas.currentTimeTxtObj, data['cur_time'])
    Text(canvas.previousTimeTxtObj, data['prev_time'])
    Text(canvas.previousMovesTxtObj, data['prev_moves'])
    Text(canvas.timeAssessmentTxtObj, data['time_score'])
    Text(canvas.movesAssessmentTxtObj, data['moves_score'])
    Text(canvas.overrallAssessmentTxtObj, data['overrall_score'])
    Text(canvas.statusTxtObj, data['status'])
    