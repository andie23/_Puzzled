from listerner import Listerner
from global_dictionary import PuzzleSessionGlobalData

class ChallengeMenuListerners(Listerner):
    def __init__(self, channel):
        listernerContainer = PuzzleSessionGlobalData().listerners
        Listerner.__init__(self, listernerContainer, channel)

class OnChallengeListChangeListerner(ChallengeMenuListerners):
    def __init__(self):
        ChallengeMenuListerners.__init__(self, 'ON_CHALLENGE_LIST_CHANGE')
    
    def onChange(self, index, challenges):
        self.updateListerners(
            lambda listerner: listerner(index, challenges)
        )

class OnStartMenuListingListerner(ChallengeMenuListerners):
    def __init__(self):
        ChallengeMenuListerners.__init__(self, 'ON_CHALLENGE_MENU_LISTING_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnCompleteMenuListListerner(ChallengeMenuListerners):
    def __init__(self):
        ChallengeMenuListerners.__init__(self, 'ON_CHALLENGE_MENU_LOAD_COMPLETE')

    def onComplete(self):
        self.updateListerners(lambda listerner: listerner())