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
        self._isAnimationStopped = False
    
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
        self._isAnimationStopped = True
    
    def isAnimationStopped(self):
        return self._isAnimationStopped
    
    def getAnimId(self):
        return 'anim_%s_%s' % (self.anim, hash(self.obj))

    def _onFrameChange(self, onstartAction=None, onfinishAction=None, onframeChangeAction=None):
        '''
        Runs actions alongside the playing animation
        '''

        def onFrameChange():
            curFrame = self.obj.getActionFrame(0)
            
            if curFrame == 0.0 and onstartAction:
                onstartAction()
            
            if curFrame >= self.fstop and onfinishAction:
                onfinishAction()
                return True
    
            if self.obj.isPlayingAction(0) and onframeChangeAction:
                onframeChangeAction(curFrame)
            return self.isAnimationStopped()

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
        self._setTimer(self._getDurationTimerId(), time, self.stop)

    def _setDelay(self, time, action):
        self._setTimer(self._getDelayTimerId(), time, action)

    def _getDurationTimerId(self):
        return 'duration_%s' % self.getAnimId()
    
    def _getDelayTimerId(self):
        return 'delay_%s' % self.getAnimId()

    def _animateObj(self, mode):
        self.obj.playAction(
            self.anim, 
            start_frame=self.fstart, 
            end_frame=self.fstop, 
            speed=self.speed,
            play_mode=mode
        )

    def unsetTimers(self):
        durationTimer = Timer(self._getDurationTimerId(), str(self.obj.scene))
        delayTimer = Timer(self._getDelayTimerId(), str(self.obj.scene))
        
        
        if durationTimer.isAlive():
            durationTimer.load()
            durationTimer.destroy()

        if delayTimer.isAlive():
            delayTimer.load()
            delayTimer.destroy()

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
