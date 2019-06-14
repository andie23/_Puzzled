from bge import logic

def detectLogicalBlocks(onDetectLogicalBlocks, space):
    logicalBlocks = space.detectLogicalBlocks()
    if logicalBlocks:
        onDetectLogicalBlocks.onDetect(logicalBlocks)

def checkMatchCount(session):
    from game_event_listerners import OnPuzzleCompleteListerner

    if session.getMatchCount() >= session.getBlockCount():
        OnPuzzleCompleteListerner().onComplete()

def decrementMatchCount(session, wasMatch):
    if wasMatch:
        session.decrementMatchCount()

def showAssessment():
    from hud_resources import loadAssessmentView
    from notification import showNotification
    from timer import Timer
    from player import getPlayerName

    showNotification('Congraturations %s !!' % getPlayerName(), duration=5.0)
    timer = Timer('assessment_preview', 'MAIN')
    timer.setTimer(6.0, loadAssessmentView)
    timer.start()

def evaluateMatch(block):
    from block_listerners import OnMatchListerner, OnMisMatchListerner
    
    wasMatch = block.isMatch
    if block.evaluateMatch():
        OnMatchListerner().onMatch(block)
    else:
        OnMisMatchListerner().onMisMatch(block, wasMatch)

def evaluateMatchStreak(session):
    accumulatedMatches = session.getAccumulatedMatchStreakCount()
    bechmarkAccumulatedMatches = session.getBenchmarkStreakCount()

    if (accumulatedMatches > 1 and 
        accumulatedMatches > bechmarkAccumulatedMatches):
        session.updateMatchStreakBenchmark()
        return True
    return False

def buildStreakCount(session):
    session.incrementMatchStreakCount()

def resetMatchstreak(session):
    from notification import showNotification
    
    if evaluateMatchStreak(session):
        showNotification(
            'WOW!! %s Match streaks in a row.. Keep it up!!' 
            % session.getAccumulatedMatchStreakCount()
        )
    session.resetMatchStreakCount()