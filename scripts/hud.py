#################################################
# Author: Andrew Mfune
# Date: 04/07/2018
# Description: All HUD objects have they're 
#              logic resides here.
#################################################
from bge import logic
from objproperties import ObjProperties
from utils import frmtTime

scene = logic.getCurrentScene()
txtres = 4

def clockMain(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_active')
    

    if isActive:
        timer = var.getProp('timer')
        _setText(own, var, frmtTime(timer), 19)
    else:
        snapshot = var.getProp('snapshot')
        _setText(own, var, frmtTime(snapshot), 19)

def _setText(own, propObj, txt, spacing=0):
    istxtFieldLocked = propObj.getProp('lock_txt')
    own.resolution = txtres
    
    if not istxtFieldLocked:
        if spacing > 0 :
            txtspace = '{:>%s}' % spacing
            txt = txtspace.format(txt)
        
        propObj.setProp('Text', txt)