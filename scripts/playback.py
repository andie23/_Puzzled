from bge import logic
from always_instance import AlwaysInstance

class PlayBack():
    def __init__(self, obj, animation, fstart, fstop, speed=1.0):
        self.obj = obj
        self.anim = animation
        self.fstart = fstart
        self.fstop = fstop
        self.speed = speed
    
    def play(self, onstartAction=None, onfinishAction=None, frameMonitor=None):
        '''
        Play animation only once.
        '''
        self._start(
            logic.KX_ACTION_MODE_PLAY, onstartAction, 
            onfinishAction, frameMonitor
        )

    def playLoop(self, onstartAction=None, onfinishAction=None, frameMonitor=None):
        '''
        Play animation on repeat
        '''
        
        self._start(
            logic.KX_ACTION_MODE_LOOP, onstartAction, 
            onfinishAction, frameMonitor
        )
       
    def stop(self):
        self.obj.stopAction(0)

    def pause(self):
        #TODO: pause current playing animation
        pass

    def resume(self):
        #TODO: resume paused animation
        pass

    def getAnimId(self):
        return 'anim_%s_%s' % (self.anim, hash(self.obj))

    def _runAnimFrameChecker(self, obj, duration, onstart, onfinish, frameMonitor=None):
        '''
        Run modules either when an animation starts or when an animation completes.
        '''
        
        curFrame = obj.getActionFrame(0)
        if curFrame >= 1.0 and onstart:
            onstart()
        
        if curFrame >= duration and onfinish:
            onfinish()
            return True
        
        if frameMonitor and obj.isPlayingAction(0):
            frameMonitor(curFrame)
        return False

    def _start(self, playMode, onstartAction, onfinishAction, frameMonitor=None):
        # check if actions are set to run at the start of the animation
        # or at the end
        if onstartAction or onfinishAction:
            # Add action in an Always Instance(loop) to constantly
            # check the current animation frame inorder to excute
            # starting and ending actions.
            alwaysInstance = AlwaysInstance(
                self.getAnimId(), self.obj.scene
            )

            alwaysInstance.addInstance(
                lambda: self._runAnimFrameChecker(
                    self.obj, self.fstop, onstartAction, 
                    onfinishAction, frameMonitor 
                )
            )
        self.obj.playAction(
            self.anim, start_frame=self.fstart, 
            end_frame=self.fstop, speed=self.speed,
            play_mode=playMode
        )
