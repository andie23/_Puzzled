from bge import logic
from canvas import NotificationCanvas
from timer import Timer
from widgets import Text
from navigator import SceneHelper
from objproperties import ObjProperties

def showNotification(message, duration=5.0, callback=None):
    notificationId = 'hud_notification'
    scene = SceneHelper(logic).getscene('HUD')
    node = scene.objects['notification_position_node']
    notification = NotificationCanvas('HUD')
    timer = Timer(notificationId, 'HUD')

    if notification.isset():
        notification.load()
        notification.easeIn()
    else:
        notification.add(node)
        notification.flyIn()

    
    Text(notification.infoTxtObj, message)
    onfinish = lambda: notification.flyOut(callback)

    if timer.isAlive():
        timer.load()
        timer.destroy()
        timer = Timer(notificationId, 'HUD')
        timer.setTimer(duration, onfinish)
        timer.start()
    else:
        timer.setTimer(duration, onfinish)
        timer.start()