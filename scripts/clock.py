from bge import logic
from datetime import timedelta
from objproperties import ObjProperties


def showTime(controller):
    own = controller.owner
    props = ObjProperties(own)
    timer = props.getProp('time')
    props.setProp('Text', formatTimer(timer))

def formatTimer(timer):
    time = str(timedelta(seconds=timer))
    return time[:7]