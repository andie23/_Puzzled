from bge import logic
from always_instance import AlwaysInstance
from timer import Timer

class PlayBack():
    '''
    Animation wrapper for GameObjects.

    Benefits offered beyond the basic animation api provided by blender include:
        1. Adding callbacks to animations (OnStart, OnFinish, OnFrameChange)
        2. Delaying animation for a set number of time
        3. Runnning animation for a duration of time before it's stopped
        4. Pausing and resuming animations (Coming soon!)
    '''

    def __init__(self, obj, animation, fstart, fstop, speed=1.0):
        self.obj = obj
        self.anim = animation
        self.fstart = fstart
        self.fstop = fstop
        self.speed = speed
    
    def play(self, onstartAction=None, onfinishAction=None, 
             onframeChangeAction=None, duration=0.0, delay=0.0):
        '''
        Play animation only once.
        '''
        self._initAnimation(
            logic.KX_ACTION_MODE_PLAY, duration, delay, onstartAction, 
            onfinishAction, onframeChangeAction
        )

    def playLoop(self, onstartAction=None, onfinishAction=None, 
                  onframeChangeAction=None, duration=0.0, delay=0.0):
        '''
        Play animation on repeat
        '''

        self._initAnimation(
            logic.KX_ACTION_MODE_LOOP, duration, delay, onstartAction,
            onfinishAction, onframeChangeAction
        )
       
    def stop(self):
        self.obj.stopAction(0)

    def getAnimId(self):
        return 'anim_%s_%s' % (self.anim, hash(self.obj))

    def _onFrameChange(self, onstartAction=None, onfinishAction=None, onframeChangeAction=None):
        '''
        Runs actions alongside the playing animation
        '''

        def onFrameChange():
            curFrame = self.obj.getActionFrame(0)
            if curFrame >= 1.0 and onstartAction:
                onstartAction()
            
            if curFrame >= self.fstop and onfinishAction:
                onfinishAction()
                return True
    
            if self.obj.isPlayingAction(0) and onframeChangeAction:
                onframeChangeAction(curFrame)
            return False

        # Add onFrameChange to an Always Instance to constantly check
        # the current frame the Game object is playing.
        alwaysInstance = AlwaysInstance(self.getAnimId(), self.obj.scene)
        alwaysInstance.addInstance(onFrameChange)

    def _setTimer(self, id, time, action):
        timer = Timer(id, str(self.obj.scene))
        if timer.isAlive():
            timer.destroy()

        if (time >= 1.0):
            timer.setTimer(time, action)
            timer.start()

    def _setDuration(self, time):
        timerId = 'duration_%s' % self.getAnimId()
        self._setTimer(timerId, time, self.stop)

    def _setDelay(self, time, action):
        timerId = 'delay_%s' % self.getAnimId()
        self._setTimer(timerId, time, action)

    def _animateObj(self, mode):
        self.obj.playAction(
            self.anim, 
            start_frame=self.fstart, 
            end_frame=self.fstop, 
            speed=self.speed,
            play_mode=mode
        )

    def _initAnimation(self, playMode, duration=0.0, delay=0.0, onstartAction=None, 
                onfinishAction=None, onFrameChange=None):
        
        def playAnimation():
            '''
            Play animation along with actions if set
            '''

            if onstartAction or onfinishAction or onFrameChange:
                self._onFrameChange(onstartAction, onfinishAction, onFrameChange)
            self._animateObj(playMode)
    
        def setDuration():
            '''
            play animation until stopped after a period of time
            '''
            playAnimation()
            self._setDuration(duration)
        
        if delay >= 1.0 and duration >= 1.0:
            self._setDelay(delay, setDuration)
            return

        if delay >= 1.0:
            self._setDelay(delay, playAnimation)
            return
    
        if duration >= 1.0:
            setDuration()
            return

        playAnimation()