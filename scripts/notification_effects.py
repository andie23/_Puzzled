from playback import PlayBack

def flyIn(obj, onstart=None, onfinish=None):
    _animate(
        obj, 'not_diag_fly_in', 0.0, 20.0, 
        0.7, onstart, onfinish
    )

def flyOut(obj, onstart=None, onfinish=None):
    _animate(
        obj, 'not_diag_fly_out', 0.0, 20.0, 
        0.7, onstart, onfinish
    )

def _animate(obj, anim, fstart, fstop, speed, onstart=None, onfinish=None):
    PlayBack(
        obj=obj, animation=anim, fstart=fstart,
        fstop=fstop, speed=speed
    ).play(
        onstart, onfinish
    )
