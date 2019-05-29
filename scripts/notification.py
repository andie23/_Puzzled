from bge import logic
from notification_canvas import NotificationCanvas
from timer import Timer
from text_widget import Text
from navigator import SceneHelper
from objproperties import ObjProperties
from notification_effects import *
from canvas_effects import fadeIn, fadeOut
HUD_NOTIFICATION_ID = 'hud_dialogue_notification'

def showNotification(message, duration=8.0, callback=None, sound=None):
    def onFinish(notification, timer):
        from audio_files import NOTIFICATION_CHIME
        from audio import Audio
        timer.setTimer(duration, lambda:fadeOut(notification,
             onFinishAction=notification.remove))
        timer.start()
        Audio(NOTIFICATION_CHIME).play()
        
    scene = SceneHelper(logic).getscene('HUD')
    notification = NotificationCanvas('HUD')
   
    if not notification.isset():
       notification.add(scene.objects['notification_position_node'], False)
    
    timer = Timer(HUD_NOTIFICATION_ID, 'HUD')
    
    if timer.isAlive():
        timer.load()
        timer.destroy()

    Text(
        notification.infoTxtObj, text=message,
        limit=80, width=30
    )
    fadeIn(notification, onFinishAction=lambda:onFinish(notification, timer))

