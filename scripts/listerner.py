from bge import logic
from logger import logger

log = logger()

class Listerner():
    def __init__(self, channel):
        gdict = logic.globalDict
        if 'listerners' not in gdict:
            gdict['listerners'] = {}
        
        if channel not in gdict['listerners']:
            gdict['listerners'][channel] = {}
            log.debug('Created listener %s', channel)
        self.listerners = gdict['listerners'][channel]
    
    def attach(self, id, action):
        if id not in self.listerners:
            self.listerners[id] = action

    def detach(self, id):
        if id not in self.listerners:
            del self.listerners[id]
    
    def getListerners(self):
        return self.listerners
    
    def updateListerners(self, callback):
        for id, listerner in self.listerners.items():
            try:
                callback(listerner)
            except Exception as error:
                log.debug('Error "%s" while running listerner %s', error, id)