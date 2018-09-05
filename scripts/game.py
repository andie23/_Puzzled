from bge import logic
from navigator import *
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
    from block import SpaceBlock
    clock = Clock(logic)
    sblock = SpaceBlock(logic.getCurrentScene())
    clock.stop()
    sblock.lock()
    writeToSessionVar('time', clock.snapshot)
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

def getSession():
    if 'session' in logic.globalDict:
        return logic.globalDict['session']
    return None

def getSessionVar(var):
    session = getSession()
    if var in session:
        return session[var]
    return None

def writeToSessionVar(var, val):
    if 'session' not in logic.globalDict:
        return
    session = logic.globalDict['session']
    if var in session:
        session[var] = val

def getstatus():
    if 'GameStatus' in logic.globalDict:
        return logic.globalDict['GameStatus']
    return None