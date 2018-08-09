from bge import logic
from canvas import DialogCanvas
from widgets import Button, Text
from navigator import *
from game import *

def pauseDialog():
    if 'pause_dialog_data' not in logic.globalDict:
        return

    canvas = DialogCanvas(logic)
    canvas.load('pause_dialog')
    title = logic.globalDict['pause_dialog_data']['title']
    subtitle = logic.globalDict['pause_dialog_data']['subtitle']
    
    Text(canvas.titleTxtObj, title).tabSpaces(45)
    Text(canvas.subtitleTxtObj, subtitle).tabSpaces(80)

    returnBtn =  Button(canvas.returnBtnObj, logic)
    homeBtn = Button(canvas.homeBtnObj, logic)
    reshuffleBtn = Button(canvas.shuffleBtnObj, logic)

    returnBtn.setOnclickAction(resume)
    homeBtn.setOnclickAction(navToChallenges)
    reshuffleBtn.setOnclickAction(reshuffle)