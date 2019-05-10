from global_dictionary import *
from navigator import navToPuzzle, overlayChallengeView
from challenge_menu_listerners import OnChallengeListChangeListerner

def __startGame(challenge):
    ActiveChallengeGlobDictData().create(challenge)
    navToPuzzle()

def playAction(challenge):
    if 'instructions' in challenge:
        overlayDialog()
        return infoDialog(
            title =challenge['name'],
            subtitle =challenge['instructions'],
            callback = lambda: __startGame(challenge)
        )
    __startGame(challenge)

def showChallengeViewer(scene, challenge):
    ChallengeViewGlobDictData().create(scene, challenge)
    overlayChallengeView()

def nextChallengeList(paginator, positionNodes):
    paginator.load()
    paginator.next()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

def previousChallengeList(positionNodes):
    paginator.load()
    paginator.previous()
    OnChallengeListChangeListerner().onChange(
        paginator.curIndex,  paginator.get()
    )

