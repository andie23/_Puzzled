from bge import logic
from button_widget import Button
from text_widget import Text
from canvas_effects import dialogPopIn
from scene_helper import SceneGlobalData

def confirm(title, subtext):
    '''
     Decorator shows confirmation dialog before executing a function.
    '''
    def main(func):
        def confirmAction(*args, **kwargs):
            action = lambda: func(*args, **kwargs)
            confirmDialog(title, subtext, action)
        return confirmAction
    return main

def getPopupMenu(canvas):
    from menu import PopUpMenu, FRONT_POSITION_NODE

    return PopUpMenu(canvas, FRONT_POSITION_NODE)

def infoDialog(title, subtitle, callback):
    from info_dialog_canvas import InfoDialogCanvas
    
    dialog = getPopupMenu(InfoDialogCanvas())
    Text(dialog.canvas.titleTxtObj, text=title.strip(), limit=15, width=20)
    Text(dialog.canvas.subtitleTxtObj, text=subtitle.strip(), limit=250, width=35)
    confirmBtn = Button(dialog.canvas.confirmBtnObj)
    confirmBtn.setOnclickAction(lambda: dialog.close(callback))
    dialog.open()

def confirmDialog(title, subtitle, onConfirm, onCancel=lambda:()):
    from confirm_dialog_canvas import ConfirmDialogCanvas

    dialog = getPopupMenu(ConfirmDialogCanvas())
    Text(dialog.canvas.titleTxtObj, title)
    Text(dialog.canvas.subtitleTxtObj, subtitle)
    confirmBtn = Button(dialog.canvas.confirmBtnObj)
    cancelBtn = Button(dialog.canvas.cancelBtnObj)

    confirmBtn.setOnclickAction(lambda: dialog.close(onConfirm))
    cancelBtn.setOnclickAction(dialog.close)
    dialog.open()
