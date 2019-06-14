from canvas import Canvas

class InfoDialogCanvas(Canvas):
    def __init__(self):
        super(InfoDialogCanvas, self).__init__(
             'info_dialog_canvas', 'info_dialog_canvas', 'HUD'
        )

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_info_dialog_title')
    
    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_info_dialog_subtext')
    
    @property
    def confirmBtnObj(self):
        return self._getWidget('btn_info_dialog_ok')
