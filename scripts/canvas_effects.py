from bge import logic
from playback import PlayBack

def dialogPopIn(canvas, onStartAction=lambda:(),
     onFinishAction=lambda:()):
    from audio_files import UI_MAXIMISE_WOOSH
    _animateCanvas(
        canvas, False, 'dialog_pop_in', 0.0, 2.0, 0.1, 
        UI_MAXIMISE_WOOSH, onStartAction, onFinishAction
    )

def fadeIn(canvas, speed=0.12, onStartAction=lambda:(),
        onFinishAction=lambda:()): 
    from audio_files import UI_MAXIMISE_WOOSH

    _animateCanvas(
        canvas=canvas, isAnimateChildren=True, anim='fade_in', 
        fstart=0.0, fstop=5.0, speed=speed, sound='', onStartAction=onStartAction,
        onFinishAction=onFinishAction
    )

def _animateCanvas(canvas, isAnimateChildren, anim, fstart, fstop, speed, sound,
         onStartAction=lambda:(), onFinishAction=lambda:()):
    
    def runStartAction(canvas):
        onStartAction()
        canvas.show(canvas.canvasObj)
    
    def runFinishAction():
        from audio import Audio

        onFinishAction()
        if sound:
            Audio(sound).play()

    def animate(obj, speed, startAction=None, finishAction=None):
        PlayBack(
            obj=obj, animation=anim, fstart=fstart, fstop=fstop,
            speed=speed
        ).play(
            startAction, finishAction
        )
    
    canvasObj = canvas.canvasObj
    if isAnimateChildren:
        # Apply animation to all unhidden children in the canvas
        for child in canvasObj.childrenRecursive:
            if '_hidden' not in child:
                # show child object if it's not visible on the screen
                animate(child, speed, canvas.show(child))
    
    # Animate the canvas container. Any start/finish action passed on should be 
    # run once after the canvas finishes animation i.e Audio or cleanup stuff
    animate(canvasObj, speed, lambda: runStartAction(canvas),
            lambda: runFinishAction())


