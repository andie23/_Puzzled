from bge import logic
from canvas import NotificationCanvas
from timer import Timer
from text_widget import Text
from navigator import SceneHelper
from objproperties import ObjProperties
from notification_effects import *
from canvas_effects import fadeIn
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
        fadeIn(notification, speed=0.8,
            onStartAction=lambda:beforeLoad(message, notification), 
            onFinishAction=lambda:afterLoad(duration, notification)
        )    
