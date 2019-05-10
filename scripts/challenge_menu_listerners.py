from listerner import Listerner

class OnChallengeListChangeListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_CHALLENGE_LIST_CHANGE')
    
    def onChange(self, index, challenges):
        self.updateListerners(
            lambda listerner: listerner(index, challenges)
        )

class OnStartMenuListingListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_CHALLENGE_MENU_LISTING_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnCompleteMenuListListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ON_CHALLENGE_MENU_LOAD_COMPLETE')

    def onComplete(self):
        self.updateListerners(lambda listerner: listerner())