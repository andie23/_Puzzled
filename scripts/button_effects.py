def clickAnimation(button, callback):
    from playback import PlayBack
    
    PlayBack(obj=button.buttonObj, animation='click', 
        fstart=0.0, fstop=10.0, speed=1.5).play(
        onfinishAction=callback
    )
