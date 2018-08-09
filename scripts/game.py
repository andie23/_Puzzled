from bge import logic
from navigator import *

def reshuffle():
    shelper = SceneHelper(logic)
    closeInDialogScreen()
    shelper.restart(['MAIN', 'HUD'])

def pause():
    shelper = SceneHelper(logic)
    shelper.pause(['MAIN', 'HUD'])
    overlayPauseDialog({
        'title': 'PAUSE', 
        'subtitle': 'Game has been paused...'
    })

def resume():
    closeInDialogScreen()
    shelper = SceneHelper(logic)
    shelper.resume(['MAIN', 'HUD'])
    