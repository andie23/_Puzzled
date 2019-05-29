from bge import logic
from playback import PlayBack

def dialogPopIn(canvas, onStartAction=lambda:(),
     onFinishAction=lambda:()):
    from audio_files import UI_MAXIMISE_WOOSH
    _animateCanvas(
        canvas, False, 'dialog_pop_in', 0.0, 2.0, 0.1, 
        UI_MAXIMISE_WOOSH, onStartAction, onFinishAction
    )

def fadeOut(canvas, speed=0.5, onStartAction=lambda:(),
        onFinishAction=lambda:()): 
    _fade(canvas, 'fade_out', speed, onStartAction, onFinishAction)

def fadeIn(canvas, speed=0.5, onStartAction=lambda:(),
        onFinishAction=lambda:()): 
    _fade(canvas, 'fade_in', speed, onStartAction, onFinishAction)

def _fade(canvas, anim, speed, onStartAction,
        onFinishAction):
    _animateCanvas(
        canvas=canvas, isAnimateChildren=True, anim=anim, 
        fstart=0.0, fstop=5.0, speed=speed, sound='', onStartAction=onStartAction,
        onFinishAction=onFinishAction
    )
def _animateCanvas(canvas, isAnimateChildren, anim, fstart, fstop, speed, sound,
         onStartAction=lambda:(), onFinishAction=lambda:()):
    
    def runStartAction():
        onStartAction()
        canvas.show()

    def runFinishAction():
        from audio import Audio

        onFinishAction()
        if sound:
            Audio(sound).play()

    PlayBack(
        obj=canvas.getCanvasObj(), 
        animation=anim, 
        fstart=fstart, 
        fstop=fstop,
        speed=speed
    ).play(
        lambda:runStartAction(), 
        lambda: runFinishAction()
    )


