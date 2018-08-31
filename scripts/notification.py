from bge import logic
from canvas import NotificationCanvas
from clock import Clock
from widgets import Text
from navigator import SceneHelper
from objproperties import ObjProperties

def showNotification(message, duration=25.0):
    shelper = SceneHelper(logic)
    scene = shelper.getscene('HUD')
    node = scene.objects['notification_position_node']
    notification = NotificationCanvas(logic, 'HUD')
    

    if not notification.isset():
        notification.add('chain_notification', node)
    else:
        notification.load('chain_notification')

    timer = Clock(logic=logic, timerObj=notification.canvasObj)
    if timer.isActive:
        timer.reset()
    else:
        timer.start()

    notification.setDuration(duration)
    Text(notification.infoTxtObj, message)

def validateExpiry(controller):
    ownObj = controller.owner
    own = ObjProperties(ownObj)
    if not own.getProp('is_timer_active'):
        return
    
    timeLimit = own.getProp('duration')
    curTime = own.getProp('timer')

    if curTime >= timeLimit:
        ownObj.endObject()
