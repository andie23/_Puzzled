class HudClockListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'HUD_CLOCK')
    
    def update(self, curTime):
        self.updateListerners(lambda listerner: listerner(curTime))

class OnloadHudListerner(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'ONLOAD_HUD')
    
    def onload(self):
        self.updateListerners(lambda listerner: listerner())