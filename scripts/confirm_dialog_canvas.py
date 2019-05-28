from canvas import Canvas

class ConfirmDialogCanvas(Canvas):
    def __init__(self, sceneID=None):
        super(ConfirmDialogCanvas, self).__init__(
            'confirmation_dialog_canvas', 'confirmation_dialog_canvas', sceneID
        )

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_confir_dialog_title')
    
    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_confir_dialog_subtext')
    
    @property
    def confirmBtnObj(self):
        return self._getWidget('btn_confir_dialog_ok')
    
    @property
    def cancelBtnObj(self):
        return self._getWidget('btn_confir_dialog_no')
