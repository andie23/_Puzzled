from bge import logic
from canvas import *
from widgets import Button, Text
from navigator import *
import game

def main():
    if logic.nextDialog:
        execDialog = logic.nextDialog
        execDialog()
        logic.nextDialog=None
    return True

# decorator function for wrapping actions with 
# confirmation action
def confirm(title, subtext):
    def main(func):
        def accept(action):
            closeDialogScreen()
            return action()

        def cancel(*args, **kwargs):
            if  game.getGameStatus() == 'PAUSED':
                return game.pause()
            closeDialogScreen()

        def dialog(*args, **kwargs):
            overlayDialog()
            execFunc = lambda: func(*args, **kwargs)
            return confirmDialog(
                title, subtext, accept, cancel, execFunc
            )
        return dialog
    return main

def confirmDialog(title, subtitle, confirmAction,
         cancelAction, *args, **kwargs):
    dialog = lambda: loadConfirmDialog(
         title, subtitle, confirmAction,
         cancelAction, *args, **kwargs
    )
    logic.nextDialog = dialog

def infoDialog(title, subtitle, callback, *args, **kwargs):
    dialog = lambda: loadInfoDialog(
         title, subtitle, callback, *args, **kwargs
    )
    logic.nextDialog = dialog

def pauseDialog():
    dialog = lambda: loadPauseDialog()
    logic.nextDialog = dialog

def puzzledDialog(title='You Are Puzzled!!', subtitle='Try Again'):
    dialog = lambda: loadPuzzledDialog(title, subtitle)
    logic.nextDialog = dialog

def getPositionNode():
    scene = logic.getCurrentScene() 
    return scene.objects['dialog_position_node']

def loadPuzzledDialog(title, subtitle):
    dialog = PuzzledDialogCanvas('DIALOG')
    dialog.add(getPositionNode())
    Text(dialog.titleTxtObj, title)
    Text(dialog.subtitleTxtObj, subtitle)

    homeBtn = Button(dialog.homeBtnObj, logic)
    reshuffleBtn = Button(dialog.shuffleBtnObj, logic)

    homeBtn.setOnclickAction(game.quit)
    reshuffleBtn.setOnclickAction(game.reshuffle)
    dialog.popIn()

def loadInfoDialog(title, subtitle, callback, *args, **kwargs):   
    dialog = InfoDialogCanvas('DIALOG')
    dialog.add(getPositionNode())
    Text(dialog.titleTxtObj, text=title.strip(), limit=15, width=20)
    Text(dialog.subtitleTxtObj, text=subtitle.strip(), limit=250, width=35)
    confirmBtn = Button(dialog.confirmBtnObj, logic)
    confirmBtn.setOnclickAction(callback, *args, **kwargs)
    dialog.popIn()

def loadPauseDialog():
    dialog = PauseDialogCanvas('DIALOG')
    dialog.add(getPositionNode())
    playBtn = Button(dialog.returnBtnObj, logic)
    playBtn.setOnclickAction(game.resume)
    dialog.popIn()

def loadConfirmDialog(title, subtitle, confirmAction,
         cancelAction, *args, **kwargs):

    dialog = ConfirmDialogCanvas('DIALOG')
    dialog.add(getPositionNode())

    Text(dialog.titleTxtObj, title)
    Text(dialog.subtitleTxtObj, subtitle)

    confirmBtn = Button(dialog.confirmBtnObj, logic)
    cancelBtn = Button(dialog.cancelBtnObj, logic)

    confirmBtn.setOnclickAction(confirmAction, *args, **kwargs)
    cancelBtn.setOnclickAction(cancelAction, *args, **kwargs)
    dialog.popIn()