from listerner import Listerner

class ChallengeMenuListerner(Listerner):
    def __init__(self, channel):
        from session_listerner_global_data import SessionListernerData
        super(ChallengeMenuListerner, self).__init__(SessionListernerData(channel))

class OnChallengeListChangeListerner(ChallengeMenuListerner):
    def __init__(self):
        super(OnChallengeListChangeListerner, self).__init__('ON_CHALLENGE_LIST_CHANGE')

    def onChange(self, index, challenges):
        self.updateListerners(
            lambda listerner: listerner(index, challenges)
        )

class OnStartMenuListingListerner(ChallengeMenuListerner):
    def __init__(self):
        super(OnStartMenuListingListerner, self).__init__('ON_CHALLENGE_MENU_LISTING_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnCompleteMenuListListerner(ChallengeMenuListerner):
    def __init__(self):
        super(OnCompleteMenuListListerner, self).__init__('ON_CHALLENGE_MENU_LOAD_COMPLETE')

    def onComplete(self):
        self.updateListerners(lambda listerner: listerner())
