from bge import logic
from objproperties import ObjProperties

def onBtnHover(controller):
    own = controller.owner
    msHover = controller.sensors['hover']
    btnIcon = own.children[0]
    
    if msHover.positive:
        btnIcon.color = [1.0, 1.0, 1.0, 0.6]
    else:
        btnIcon.color = [1.0, 1.0, 1.0, 1.0]

def onBtnClick(controller):
    own = controller.owner
    msHover = controller.sensors['hover']
    msClick = controller.sensors['click']
    btnProps = ObjProperties(own)
    gdict = logic.globalDict
   
    btnName = btnProps.getProp('btnID')
    if msHover.positive and msClick.positive:
        if btnName in gdict:
            btnLogic = gdict[btnName]
            command = btnLogic['command']
            command()