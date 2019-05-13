from global_dictionary import PuzzleSessionGlobalData

class HudListerner(Listerner):
    def __init__(self, channel):
        listernerContainer = PuzzleSessionGlobalData().listerners
        Listerner.__init__(self, listernerContainer, channel)

class HudClockListerner(HudListerner):
    def __init__(self):
        HudListerner.__init__(self, 'HUD_CLOCK')
    
    def update(self, curTime):
        self.updateListerners(lambda listerner: listerner(curTime))

class OnloadHudListerner(HudListerner):
    def __init__(self):
        HudListerner.__init__(self, 'ONLOAD_HUD')
    
    def onload(self):
        self.updateListerners(lambda listerner: listerner())