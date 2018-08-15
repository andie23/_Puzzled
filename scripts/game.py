from bge import logic
from navigator import *
import dialog

@dialog.confirm('QUIT' ,'Really? you want to exit to the main menu?')
def quit():
    navToChallenges()
    logic.globalDict['GameStatus'] = 'EXITED'

@dialog.confirm('RESHUFFLE', 'Are you stuck or something? do you want to reshuffle?')
def reshuffle():
    shelper = SceneHelper(logic)
    shelper.restart(['MAIN', 'HUD'])
    logic.globalDict['GameStatus'] = 'RESTARTED'

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