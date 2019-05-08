import game
from logger import logger

log = logger()
class Listerner():
    def __init__(self, channel):
        if not game.getChannel(channel):
            game.setChannel(channel, {})
        self.listerners = game.getChannel(channel)

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
            callback(listerner)
          