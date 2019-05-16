from bge import logic
from canvas import NotificationCanvas
from timer import Timer
from widgets import Text
from navigator import SceneHelper
from objproperties import ObjProperties
from animate import *

HUD_NOTIFICATION_ID = 'hud_dialogue_notification'


def showNotification(message, duration=8.0, callback=None, sound=None):
    def beforeLoad(message, notification):
        Text(
            notification.infoTxtObj, text=message,
            limit=80, width=30
        )
        notification.show(notification.canvasObj)
        timer = Timer(HUD_NOTIFICATION_ID, 'HUD')

        if timer.isAlive():
            timer.load()
            timer.destroy()

    def afterLoad(duration, notification, sound=None):
        from audio_files import NOTIFICATION_CHIME
        from audio import Audio

        if not sound:
            sound = NOTIFICATION_CHIME

        Audio(sound).play()
        timer = Timer(HUD_NOTIFICATION_ID, 'HUD')
        timer.setTimer(duration, lambda: removeDialog(notification))
        timer.start()

    def addDialogue():
        notification = NotificationCanvas('HUD')
        scene = SceneHelper(logic).getscene('HUD')
        notification.add(scene.objects['notification_position_node'])
        return notification
    
    def removeDialog(notification):
        def onFinish():
            notification.remove()
            if callback:
                callback()

        if notification.isset():
            flyOut(notification.canvasObj, onfinish=onFinish)

    notification = NotificationCanvas('HUD')
    if not notification.isset():
        notification = addDialogue()
        flyIn(notification.canvasObj,
            onstart=lambda:beforeLoad(message, notification), 
            onfinish=lambda:afterLoad(duration, notification, sound)
        )    
    else:
        notification.load()
        fadeIn(notification.canvasObj,
            onstart=lambda:beforeLoad(message, notification), 
            onfinish=lambda:afterLoad(duration, notification)
        )    

def setActionPoints(animData, onstart=None, onfinish=None):
    if onstart:
        animData['on_start_action'] = onstart

    if onfinish:
        animData['on_finish_action'] = onfinish

    return animData

def fadeIn(canvasObj, onstart=None, onfinish=None):
     animData = {
        'scene_id' : 'HUD', 
        'target_obj' : canvasObj,
        'anim_name' : 'notification_fade_in',
        'fstart' : 0.0,
        'fstop' : 5.0,
        'speed' : 0.6
     }
     animData = setActionPoints(animData, onstart, onfinish)
     initAnimation(animData)

     for child in canvasObj.childrenRecursive:
        initAnimation({
            'scene_id' : 'HUD', 
            'target_obj' : child,
            'anim_name' : 'fade_in',
            'fstart' : 0.0,
            'fstop' : 5.0,
            'speed' : 0.4
        }, "%s_%s_child_fadein" % (canvasObj, child))

def flyIn(canvasObj, onstart=None, onfinish=None):
    animData = {
        'scene_id' : 'HUD',
        'target_obj' : canvasObj,
        'anim_name' : 'not_diag_fly_in', 
        'fstart' : 0.0,
        'fstop' : 20.0,
        'speed' : 0.7
    }
    animData = setActionPoints(animData, onstart, onfinish)
    initAnimation(animData)

def flyOut(canvasObj, onstart=None, onfinish=None):
    animData = {
        'scene_id' : 'HUD', 
        'target_obj' : canvasObj,
        'anim_name' : 'not_diag_fly_out', 
        'fstart' : 0.0,
        'fstop' : 20.0,
        'speed' : 0.7,
    }
    animData = setActionPoints(animData, onstart, onfinish)
    initAnimation(animData)