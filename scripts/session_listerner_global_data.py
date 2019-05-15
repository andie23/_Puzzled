from session_global_data import SessionGlobalData

class SessionListernerData(SessionGlobalData):
    def __init__(self, channel):
        super(SessionListernerData, self).__init__()
        self.channel = channel
        self._listerners = self.data['listerners']

    def isChannelSet(self):
        return self.channel in self._listerners

    def isListernerIdSet(self, id):
        return id in self.getChannel()

    def getChannel(self):
        return self._listerners[self.channel]
    
    def initChannel(self):
        self._listerners[self.channel] = {}
     
    def addListerner(self, id, listerner):
        self._listerners[self.channel][id] = listerner

    def removeListerner(self, id):
        del self._listerners[self.channel][id]

    def removeChannel(self):
        del self._listerners[self.channel]