from bge import logic
from objproperties import ObjProperties

def onBtnClick(controller):
    own = controller.owner
    msHover = controller.sensors['click_mouse_hover']
    msClick = controller.sensors['click_mouse_click']
    btnProps = ObjProperties(own)
    gdict = logic.globalDict
   
    btnName = btnProps.getProp('bname')
    
    if msHover.positive and msClick.positive:
        if btnName in gdict:
            btnLogic = gdict[btnName]
            command = btnLogic['command']
            print(gdict)
            if 'kwargs' in btnLogic:
                kwargs = btnLogic['kwargs']
                command(kwargs)
            else:
                command()