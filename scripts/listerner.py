from bge import logic

class Listerner():
    def __init__(self, channel):
        gdict = logic.globalDict
        if 'listerners' not in gdict:
            gdict['listerners'] = {}
            gdict['listerners'][channel] = {}
        self.listerners = gdict['listerners'][channel]
    
    def attach(self, id, action):
        if id not in self.listerners:
            self.listerners[id] = action

    def detach(self, id):
        if id not in self.listerners:
            del self.listerners[id]
    
    def getListerners(self):
        return self.listerners