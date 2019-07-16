def clickAnimation(button, callback=lambda:()):
    from playback import PlayBack
    
    PlayBack(obj=button, animation='click', 
        fstart=0.0, fstop=10.0, speed=1.0).play(
        onfinishAction=callback
    )
