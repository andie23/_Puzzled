from bge import logic
from navigator import SceneHelper

def reshuffle():
    shelper = SceneHelper(logic)
    shelper.restart(['MAIN', 'HUD'])

def pause():
    shelper = SceneHelper(logic)
    shelper.pause(['MAIN', 'HUD'])

def resume():
    shelper = SceneHelper(logic)
    shelper.resume(['MAIN', 'HUD'])
    