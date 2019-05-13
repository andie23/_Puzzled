from score import Stats, Score
from utils import frmtTime, calcPercDiff

def calculateScore(moves, time, streaks):
    '''
    A lower number is desirable for a score bacause we want the player
    to complete a challenge with less moves and time. Higher match streaks 
    help to reduce the score further to achieve a lower score.
    '''

    avg = moves + int(time)/ 2
    return avg - streaks

def getPrevScore(playerId, challengeId):
    score = Score(playerId, challengeId)
    if score.fetch():
        return score
    
def updateChallengeStats(playerId, challengeId, time, isWin=False):
    stats = Stats(playerId, challengeId)
    if not stats.fetch():
        stats.playCount = 1
        stats.loses = 0
        stats.wins = 1
        stats.totalTime = time
        stats.add()
    else:
        stats.playCount += 1
        stats.totalTime += time
        if isWin:
            stats.wins += 1
        else:
            stats.loses +=1
        stats.update()

def updateChallengeBenchmark(playerId, challengeId, moves, time, streaks, points):
    score = Score(playerId, challengeId)
    score.timeCompleted = time
    score.moves = moves
    score.streaks = streaks
    score.overallScore = points
    score.update()

def addChallengeBenchmark(playerId, challengeId, moves, time, streaks, points):
    score = Score(playerId, challengeId)
    score.timeCompleted = time
    score.moves = moves
    score.streaks = matchStreaks
    score.overallScore = points
    score.add()

def assessTime(timeBenchmark, time):
    return getPercentageDiffStatus(timeBenchmark, time)

def assessMoves(movesBenchmark, moves):
    return getPercentageDiffStatus(movesBenchmark, moves)

def assessStreaks(streakBenchmark, streaks):
    return getPercentageDiffStatus(streakBenchmark, streaks, '>')

def assessScore(scoreBenchmark, score):
    return getPercentageDiffStatus(scoreBenchmark, score)

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
