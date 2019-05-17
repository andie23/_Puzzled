from bge import logic
from animate import initAnimation

def dialogPopIn(canvas, onStartAction=lambda:(), onFinishAction=lambda:()):
    from audio_files import UI_MAXIMISE_WOOSH
    _animateCanvas(
        canvas, False, 'dialog_pop_in', 0.0, 2.0, 0.1, 
        UI_MAXIMISE_WOOSH, onStartAction, onFinishAction
    )

def _animateCanvas(canvas, isAnimateChildren, anim, fstart, fstop, speed, sound,
         onStartAction, onFinishAction):
    
    def runStartAction(canvas):
        onStartAction()
        canvas.show(canvas.canvasObj)
    
    def runFinishAction():
        from audio import Audio

        onFinishAction()
        if sound:
            Audio(sound).play()

    def animate(obj, speed, startAction=lambda:(),
                 finishAction=lambda:()):
        initAnimation({
            'scene_id' : canvas.sceneName, 
            'target_obj' : obj,
            'anim_name' : anim, 
            'fstart' : fstart,
            'fstop' : fstop,
            'speed' : speed,
            'on_start_action': startAction,
            'on_finish_action' : finishAction
        })
    
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


