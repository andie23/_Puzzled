def clickAnimation(button, scene, callback):
    from animate import initAnimation

    initAnimation({
        'scene_id' : str(scene),
        'target_obj' : button.buttonObj,
        'anim_name' : 'click',
        'fstart' : 1.0,
        'fstop' : 10.0,
        'speed' : 1.8,
        'on_finish_action' : callback
    })
