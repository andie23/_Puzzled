from bge import logic
from datetime import timedelta
from objproperties import ObjProperties


scene = logic.getCurrentScene()
tmObj = scene.objects['timeObj']
props = ObjProperties(tmObj)

def showTime(controller):
    timer = props.getProp('time')
    props.setProp('Text', formatTimer(timer))

def getCurTime():
    return props.getProp('time')

def formatTimer(timer):
    time = str(timedelta(seconds=timer))
    return time[:7]