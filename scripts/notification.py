from bge import logic
from canvas import NotificationCanvas
from clock import Clock
from widgets import Text
from navigator import SceneHelper
from objproperties import ObjProperties

def showNotification(message, duration=5.0, callback=None):
    shelper = SceneHelper(logic)
    scene = shelper.getscene('HUD')
    node = scene.objects['notification_position_node']
    notification = NotificationCanvas(logic, 'HUD')

    if not notification.isset():
        notification.add('hud_notification', node)
        notification.flyIn()
    else:
        notification.load('hud_notification')
        notification.fadeIn()

    timer = Clock(logic=logic, timerObj=notification.canvasObj)
    if timer.isActive:
        timer.reset()
    else:
        timer.start()
    
    if callback:
        notification.setCallback(callback)
    
    notification.setDuration(duration)
    Text(notification.infoTxtObj, message)

def validateExpiry(controller):
    ownObj = controller.owner
    own = ObjProperties(ownObj)
    timer = Clock(logic=logic, timerObj=ownObj)    
    timeLimit = own.getProp('duration')

    if timer.isActive and timer.curtime() >= timeLimit:
        timer.stop()
        notification = NotificationCanvas(logic, 'HUD')
        notification.load('chain_notification')
        
        if own.getProp('callback') is not None:
            notification.flyOut(own.getProp('callback'))
        else:
            notification.flyOut()
