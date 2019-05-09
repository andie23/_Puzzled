from bge import logic
import aud

class Audio():
    def __init__(self, sound):
        self.sound = sound
        self.device = aud.device()
        self.factory = aud.Factory(sound)
        self.soundHandler = None

    def play(self):
        self.soundHandler = self.device.play(self.factory)
    
    def stop(self):
        self.__runSoundHandler('stop')
    
    def pause(self):
        self.__runSoundHandler('pause')

    def resume(self):
        self.__runSoundHandler('resume')

    def __runSoundHandler(self, action):
        if self.soundHandler is None:
            return
        
        if action == 'stop':
            self.soundHandler.stop()
        
        elif action == 'pause':
            self.soundHandler.pause()

        elif action == 'resume':
            self.soundHandler.resume()
        

