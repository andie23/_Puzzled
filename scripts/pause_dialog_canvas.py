from canvas import Canvas

class PauseDialogCanvas(Canvas):
    def __init__(self, sceneID=None):
        super(PauseDialogCanvas, self).__init__(
            'pause_dialog_canvas', 'pause_dialog_canvas', sceneID
        )

    @property
    def shuffleBtnObj(self):
        return self._getWidget('btn_pause_dialog_reshuffle')
   
    @property
    def returnBtnObj(self):
        return self._getWidget('btn_pause_dialog_play')
