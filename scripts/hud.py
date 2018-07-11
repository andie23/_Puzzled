#################################################
# Author: Andrew Mfune
# Date: 04/07/2018
# Description: All HUD objects have they're 
#              logic resides here.
#################################################
from bge import logic
from objproperties import ObjProperties
from utils import frmtTime, positionTxt

scene = logic.getCurrentScene()
txtres = 4

def clockMain(controller):
    own = controller.owner
    own.resolution = txtres
    var = ObjProperties(own)
    isActive = var.getProp('is_active')

    if isActive:
        curTime = var.getProp('timer')
        frmtedCurTime = positionTxt(frmtTime(curTime), right=26)
        var.setProp('Text', frmtedCurTime)

def movesCountMain(controller):
    gdict = logic.globalDict
    own = controller.owner
    own.resolution = txtres
    moves = gdict['NumberOfMoves']
    var = ObjProperties(own)
    
    if not var.getProp('lock_txt'):
        var.setProp('Text', moves)