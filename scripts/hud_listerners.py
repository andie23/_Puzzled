from listerner import Listerner

class HudListerner(Listerner):
    def __init__(self, channel):
        from session_listerner_global_data import SessionListernerData
        super(HudListerner, self).__init__(SessionListernerData(channel))

class HudClockListerner(HudListerner):
    def __init__(self):
        super(HudClockListerner, self).__init__('HUD_CLOCK')
    
    def update(self, curTime):
        self.updateListerners(lambda listerner: listerner(curTime))

class OnloadHudListerner(HudListerner):
    def __init__(self):
        super(OnloadHudListerner, self).__init__('ONLOAD_HUD')

    def onload(self):
        self.updateListerners(lambda listerner: listerner())
