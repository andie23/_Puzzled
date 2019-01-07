from bge import logic
from canvas import NotificationCanvas
from timer import Timer
from widgets import Text
from navigator import SceneHelper
from objproperties import ObjProperties

IDENTIFIER  = 'hud_notification'
NODE = 'notification_position_node'

def showNotification(message, duration=5.0, callback=None):
    scene = SceneHelper(logic).getscene('HUD')
    node = scene.objects[NODE]
    notification = NotificationCanvas('HUD')
    timer = Timer(IDENTIFIER, 'HUD')

    
    if notification.isset():
        notification.load()
        notification.easeIn()
    else:
        notification.add(node)
        notification.flyIn()

    
    Text(notification.infoTxtObj, message)

    timer.setTimer(
        duration, lambda:notification.flyOut(callback)
    )

    if not timer.isAlive():
        timer.start()
    
