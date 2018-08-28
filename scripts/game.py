from bge import logic
from navigator import *
from block import SpaceBlock
from clock import Clock
import dialog

@dialog.confirm('QUIT' ,'Really? you want to exit to the main menu?')
def quit():
    navToChallenges()
    logic.globalDict['GameStatus'] = 'EXITED'

@dialog.confirm('RESHUFFLE', 'Are you stuck or something? do you want to reshuffle?')
def reshuffle():
    shelper = SceneHelper(logic)
    closeAssessmentScreen()
    shelper.restart(['MAIN', 'HUD'])
    logic.globalDict['GameStatus'] = 'RESTARTED'

@property
def status():
    return logic.globalDict['GameStatus']

def stop():
    clock = Clock(logic)
    sblock = SpaceBlock(logic.getCurrentScene())
    clock.stop()
    sblock.lock()
    logic.globalDict['GameStatus'] = 'STOPPED'

def pause():
    overlayDialog()
    shelper = SceneHelper(logic)
    shelper.pause(['MAIN', 'HUD'])
    dialog.pauseDialog(
        title='PAUSE',
        subtitle='The game is paused. Click play to continue..'
    )
    logic.globalDict['GameStatus'] = 'PAUSED'

def resume():
    shelper = SceneHelper(logic)
    shelper.resume(['MAIN', 'HUD'])
    logic.globalDict['GameStatus'] = 'RESUMED'
    closeDialogScreen()

def getstatus():
    if 'GameStatus' in logic.globalDict:
        return logic.globalDict['GameStatus']
    return None