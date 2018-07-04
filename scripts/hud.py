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

def clockMain(controller):
    own = controller.owner
    var = ObjProperties(own)
    isActive = var.getProp('is_active')
    snapshot = var.getProp('snapshot')
    timer = var.getProp('timer')

    if isActive:
        var.setProp('Text', frmtTime(timer))
    else:
        var.setProp('Text', frmtTime(snapshot))
