from bge import logic
from confirm_dialog_canvas import ConfirmDialogCanvas
from info_dialog_canvas import InfoDialogCanvas
from pause_dialog_canvas import PauseDialogCanvas
from button_widget import Button
from text_widget import Text
from canvas_effects import dialogPopIn
from hud_listerners import OnOpenDialogListerner
from hud_listerners import OnCloseDialogListerner
from ui_background import attachWhiteTransparentBg, attach_background_object

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

def getPositionNode():
    from scene_helper import Scene
    scene= Scene('HUD').getscene()
    return scene.objects['dialog_position_node']

@attach_background_object
def infoDialog(title, subtitle, callback):
    def onClick(dialog):
        OnCloseDialogListerner().onClose()
        callback()
        dialog.remove()
        
    dialog = InfoDialogCanvas()
    dialog.add(getPositionNode(), False)
    Text(dialog.titleTxtObj, text=title.strip(), limit=15, width=20)
    Text(dialog.subtitleTxtObj, text=subtitle.strip(), limit=250, width=35)
    confirmBtn = Button(dialog.confirmBtnObj)
    confirmBtn.setOnclickAction(lambda: onClick(dialog))
    dialog.show()
    OnOpenDialogListerner().onOpen()
    return dialog

@attach_background_object
def confirmDialog(title, subtitle, onConfirm, onCancel=lambda:()):
    def __onCancel(dialog):
        OnCloseDialogListerner().onClose()
        dialog.remove()
        return onCancel()

    def __onConfirm(dialog):
        OnCloseDialogListerner().onClose()
        dialog.remove()
        return onConfirm()

    dialog = ConfirmDialogCanvas()
    dialog.add(getPositionNode(), True)

    Text(dialog.titleTxtObj, title)
    Text(dialog.subtitleTxtObj, subtitle)

    confirmBtn = Button(dialog.confirmBtnObj)
    cancelBtn = Button(dialog.cancelBtnObj)

    confirmBtn.setOnclickAction(lambda: __onConfirm(dialog))
    cancelBtn.setOnclickAction(lambda: __onCancel(dialog))
    dialog.show()
    OnOpenDialogListerner().onOpen()
    return dialog