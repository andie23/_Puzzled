class Listerner():
    def __init__(self, listernerModel):
        self._listernerModel = listernerModel
        if not self._listernerModel.isChannelSet():
            self._listernerModel.initChannel()

    def attach(self, id, listerner):
        if not self._listernerModel.isListernerIdSet(id):
            self._listernerModel.addListerner(id, listerner)

    def detach(self, id):
        if self._listernerModel.isListernerIdSet(id): 
            self._listernerModel.removeListerner(id)
        
    def getListerners(self):
        return self._listernerModel.getChannel()

    def updateListerners(self, callback):
        listerners = self._listernerModel.getChannel()
        for id, listerner in listerners.items():
            callback(listerner)
          