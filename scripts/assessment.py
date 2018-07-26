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
    player = gdict['player']
    challenge = gsetup['id']
    playerID = player['id']
    title = gsetup['name']
    score = Scores(pid=playerID, challenge=challenge)
    assessment = {}
    
    if score.isset():
       assessment = assessSession(score, session)

    assessmentBuild = buildAssessment(score, session, assessment)
    updateUI(score, title, assessmentBuild)
    updateCache(score, session, assessment)

def assessSession(score, session):
    if score.isset():
        prevTime = score.timeCompleted
        prevMoves = score.moves
        prevScore = int(prevTime) + int(prevMoves)

        curTime = session['current_time']
        curMoves = session['current_moves']
        curScore = int(curTime) + int(curMoves)

        timeAssessment = assess(curTime, prevTime)
        movesAssessment = assess(curMoves, prevMoves)
        scoreAssessment = assess(curScore, prevScore)

        return {
            'time' : timeAssessment, 
            'moves': movesAssessment,
            'score' : scoreAssessment
        }
    return None

def buildAssessment(score, session, assessment={}):
    build = {}
    build.update(session)
    if score.isset():
        build.update({
            'prev_time' : score.timeCompleted,
            'prev_moves' : score.moves
        })

    for category, body in assessment.items():
        status = body['status']
        percentage = body['percentage']

        build[category] = "{0}% {1}".format(
            percentage, 'Better' if status == 1 else 'Worse'
        )
    return build

def assess(curVal, prevVal):
    if curVal < prevVal:
       percDiff =  calcPercDiff(prevVal, curVal)
       return {'status': 1, 'percentage': percDiff}
    percDiff = calcPercDiff(curVal, prevVal)
    return {'status': 0, 'percentage': percDiff}

def updateCache(score, session, assessment={}):
    moves = session['current_moves']
    time = session['current_time']
    if score.isset():
        assessmentScore = assessment['score']
        scoreStatus = assessmentScore['status']

        if scoreStatus == 1:
            score.editTime(time)
            score.editMoves(moves)
    score.add(time, moves)

def updateUI(score, title, data):
    canvas = AssessmentCanvas(logic)
    canvas.load('assessement')
    Text(canvas.titleTxtObj, title)
    Text(canvas.currentMovesTxtObj, data['current_moves'])
    Text(canvas.currentTimeTxtObj, frmtTime(data['current_time']))
    if score.isset():
        Text(canvas.previousTimeTxtObj, frmtTime(data['prev_time']))
        Text(canvas.previousMovesTxtObj, data['prev_moves'])
        Text(canvas.timeAssessmentTxtObj, data['time'])
        Text(canvas.movesAssessmentTxtObj, data['moves'])
        Text(canvas.overrallAssessmentTxtObj, data['score'])
        if data['score'] == 1:
            Text(canvas.statusTxtObj, 'Congrats, new Benchmark Set!!')
        else:
            Text(canvas.statusTxtObj, ':(')
    else:
        Text(canvas.statusTxtObj, 'Congrats, new Benchmark Set!!')
