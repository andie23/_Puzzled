from global_dictionary import *
from challenge_menu_listerners import OnChallengeListChangeListerner

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

